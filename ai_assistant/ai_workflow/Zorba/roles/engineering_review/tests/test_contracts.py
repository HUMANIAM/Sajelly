"""Contract tests are executable rules, not tests of LLM review intelligence."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from review_contract import validate, render_response  # noqa: E402


def example(stack: str, name: str) -> dict:
    return json.loads((ROOT/stack/'examples'/f'{name}.json').read_text(encoding='utf-8'))


class ReviewContractTests(unittest.TestCase):
    def test_valid_request_and_all_three_example_decisions_for_both_specialists(self):
        # Given: supplied complete schema-conformant synthetic examples
        # When: the independent reviewers' contracts are validated
        # Then: request, approval, blocking and evidence-gap responses pass
        for stack in ('frontend','backend'):
            with self.subTest(stack=stack):
                req=example(stack,'request')
                validate('request',stack,req)
                for name in ('response_approve','response_block','response_missing_evidence'):
                    validate('response',stack,example(stack,name),request=req)

    def test_implementation_without_diff_is_rejected(self):
        for stack in ('frontend','backend'):
            req=example(stack,'request')
            req['change']['diff']=None
            with self.assertRaisesRegex(ValueError, 'schema invalid'):
                validate('request',stack,req)

    def test_architecture_without_changed_files_or_diff_is_allowed(self):
        for stack in ('frontend','backend'):
            req=example(stack,'request')
            req['stage']='architecture'
            req['change']={'changed_files':[],'diff':None,'artifact_refs':[{'kind':'path','location':'docs/architecture.md','purpose':'Reviewed proposal','available':True}]}
            validate('request',stack,req)

    def test_duplicate_criterion_and_missing_id_rejected_structurally(self):
        for stack in ('frontend','backend'):
            r=example(stack,'response_approve')
            r['criteria'][1]=copy.deepcopy(r['criteria'][0])
            with self.assertRaisesRegex(ValueError, 'schema invalid'):
                validate('response',stack,r)

    def test_wrong_specialist_request_or_response_rejected(self):
        for stack,other in (('frontend','backend'),('backend','frontend')):
            request=example(stack,'request')
            request['reviewer']=other
            with self.assertRaises(ValueError): validate('request',stack,request)
            response=example(stack,'response_approve')
            response['reviewer']=other
            with self.assertRaises(ValueError): validate('response',stack,response)

    def test_review_id_and_version_must_match_request(self):
        for stack in ('frontend','backend'):
            r=example(stack,'response_approve')
            r['review_id']='OTHER'
            with self.assertRaisesRegex(ValueError, 'differs from request'):
                validate('response',stack,r,request=example(stack,'request'))

    def test_blocking_finding_cannot_be_approved(self):
        for stack in ('frontend','backend'):
            r=example(stack,'response_block')
            r['decision']='approve_with_notes'
            with self.assertRaisesRegex(ValueError, 'require block'):
                validate('response',stack,r)

    def test_critical_missing_evidence_must_block(self):
        for stack in ('frontend','backend'):
            r=example(stack,'response_missing_evidence')
            r['decision']='approve'
            with self.assertRaisesRegex(ValueError, 'require block'):
                validate('response',stack,r)

    def test_missing_evidence_requires_explicit_gap(self):
        for stack in ('frontend','backend'):
            r=example(stack,'response_missing_evidence')
            r['verification_assessment']['gaps']=[]
            with self.assertRaisesRegex(ValueError, 'verification gap'):
                validate('response',stack,r)

    def test_pass_requires_actual_cited_evidence(self):
        for stack in ('frontend','backend'):
            r=example(stack,'response_approve')
            r['criteria'][0]['evidence']=[]
            with self.assertRaisesRegex(ValueError, 'pass without evidence'):
                validate('response',stack,r)

    def test_approval_cannot_hide_suggestions_questions_or_risks(self):
        for stack in ('frontend','backend'):
            r=example(stack,'response_approve')
            r['residual_risks']=[{'risk':'sample','impact':'risk','owner':'human','exit_condition':'review'}]
            with self.assertRaisesRegex(ValueError, 'approve cannot have'):
                validate('response',stack,r)

    def test_cross_stack_finding_remains_with_owning_reviewer(self):
        # Given: the frontend reviewer identifies an incompatible backend API
        # When: it reports an evidence-backed cross-stack question
        # Then: it remains a frontend review with backend ownership, not an agent switch
        r=example('frontend','response_approve')
        r['decision']='approve_with_notes'
        r['findings']=[{
            'id':'F-CROSS','severity':'question','category':'api_contract',
            'title':'Backend response contract needs confirmation',
            'owner':'backend','paths':['contracts/api.yaml'],
            'evidence':['Synthetic contract change: endpoint schema is not provided'],
            'risk':'Frontend cannot guarantee compatibility',
            'required_resolution':'Backend owner must confirm the contract',
            'verification_needed':['Contract integration check'],
            'criterion_ids':['FE-03','U-03']}]
        validate('response','frontend',r,request=example('frontend','request'))
        self.assertEqual('backend',r['findings'][0]['owner'])

    def test_findings_must_have_unique_ids_and_in_scope_criteria(self):
        r=example('backend','response_block')
        r['findings'].append(copy.deepcopy(r['findings'][0]))
        with self.assertRaisesRegex(ValueError,'identifiers must be unique'):
            validate('response','backend',r)
        r['findings'].pop()
        r['findings'][0]['criterion_ids']=['FE-01']
        with self.assertRaisesRegex(ValueError,'outside backend scope'):
            validate('response','backend',r)

    def test_markdown_render_keeps_untrusted_content_as_literal_text(self):
        r=example('frontend','response_approve')
        r['summary']='<script>alert(1)</script> **untrusted**'
        report=render_response(r)
        self.assertIn('\\<script\\>',report)
        self.assertNotIn('<script>',report)
        self.assertIn('\\*\\*untrusted\\*\\*', report)
        self.assertIn('FE-10',report)
        self.assertIn('U-08',report)
        self.assertIn('human approval separate',report)

    def test_failed_criterion_requires_a_finding(self):
        r=example('frontend','response_approve')
        r['decision']='approve_with_notes'
        r['criteria'][0]['status']='fail'
        with self.assertRaisesRegex(ValueError,'requires an evidence-backed finding'):
            validate('response','frontend',r)

    def test_blocking_finding_must_link_to_failed_or_unverified_criterion(self):
        r=example('backend','response_block')
        for c in r['criteria']:
            if c['status']=='fail': c['status']='pass'
        with self.assertRaisesRegex(ValueError,'must correspond to failed or unverified'):
            validate('response','backend',r)


if __name__=='__main__': unittest.main()
