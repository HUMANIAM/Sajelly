# سجلى (Sajelly) — Requirements

## Why Sajelly exists

My father makes and sells ovens and other products in his workshop in Egypt. Some customers pay the full price. Others pay part of it and return later with more money. He keeps track of what each person owes him in handwritten notebooks.

My father cannot read or write. Looking through notebooks, finding a customer's name, checking what they paid, and working out what remains can be difficult.

When I lived in Egypt, I helped him with this. He would tell me who bought something or who paid him, and I would help him find the right person, write it down, or work out the balance. **Sajelly should do that same job.**

It is not meant to be complicated accounting software. It is a helpful accountant my father can talk to.

## What using it should feel like

My father opens the app on his Android phone. He sees **سجلى**, a simple picture that represents the accountant, and one large microphone button. There is also a small camera button for sending pictures of notebook pages. No dashboard, menus, or tables are needed on his main screen.

He taps the microphone to speak and taps again when he finishes. Sajelly listens, understands what he wants, and answers by voice in everyday Egyptian Arabic. If Sajelly is speaking, he can stop it with the button.

He should not have to memorize commands or fill in forms. If he says something incomplete, Sajelly asks a short, natural question and remembers what they were discussing. It should ask only what it needs to help him.

The app needs internet in the first version. It should keep him signed in so he does not have to log in every day. Sign-in can be simple; we will choose the exact method later.

## The work Sajelly helps with

### Remember who owes what

Each customer has one running balance. My father may sell that person a large oven, a small oven, or something else. He does not need to match every later payment to a particular product.

- When a customer buys something without paying the full amount, the amount owed goes up.
- When a customer pays, the amount owed goes down.
- If an old notebook only says that someone owes 2,000 Egyptian pounds, Sajelly can record that as the **starting balance**, even if earlier purchases and payments are unknown.
- Sajelly keeps the individual records behind every change, so we can see how the balance was reached.

There is no customer credit in the current business. If a payment is greater than the amount owed, Sajelly should ask about it rather than recording an impossible balance.

### Know which customer we mean

Names can be repeated. A customer's first name alone may not tell us who they are.

When adding someone, Sajelly should ask for more identifying information, such as their full name or something my father knows them by. It should explain, in simple language, that a short name may cause confusion later. **If my father still wants to register the customer with only that name, Sajelly should allow it.**

Before adding a customer or recording money for someone, Sajelly checks the existing records. If several people might match, it asks my father which one he means. It must never silently pick a person, merge two people, or invent details to tell them apart.

### Answer questions, not give lectures

My father might ask:

- "أحمد عليه كام؟" — How much does Ahmed owe?
- "مين لسه عليه فلوس؟" — Who still owes me money?
- "الناس عليهم كام كلهم؟" — How much do all customers owe?
- "مين دفع الأسبوع ده؟" — Who paid this week?

Sajelly looks up the real records and gives a direct spoken answer. If he asks only for a number, it gives the number. If he asks how the balance was reached, it can explain the purchases and payments.

If many customers owe money, Sajelly can read their names and amounts one by one until the list ends or my father stops it.

**Sajelly must get financial answers from stored records. It must not guess amounts.**

### Write carefully, and never lose history

Sajelly should act like a careful human helper. It listens, checks what is already known, and asks about missing or unclear information before proposing a change.

**Nothing that changes financial records is saved without explicit confirmation.** Sajelly tells my father, in simple spoken language, exactly what it is about to record or correct, then asks if that is right. If he says no, changes the details, or has not answered clearly, it does not save the change.

The software must keep a link between the proposed change and the actual confirmation my father gave. The agent merely saying "he confirmed" is not enough. A confirmation for one change cannot be reused for another, and the same confirmed change must not be saved twice.

There is **no delete** for financial history. If my father made a mistake, Sajelly records a correction while preserving the earlier entry. We should always be able to understand what changed and why.

## Bringing the old notebooks into Sajelly

My father already has important records on paper. We should not make him start from an empty account.

At first, my sister will take photos of notebook pages and submit them through the app's simple camera option. The photos will reach me for review.

Sajelly should attempt to read each page and suggest the customers, amounts, and balances it finds. I will check the suggestions **one by one**, correcting anything wrong and confirming each entry before it becomes part of the records.

A saved entry should still point back to the photo it came from. The system must not quietly make up an unreadable name or number. We also need to check what it *missed*, not only what it extracted.

Later, my sister may review and confirm the extracted records herself. That is not required initially.

## Who uses it

- **My father** uses voice to ask questions and manage customer debts and payments. He has final control over the financial changes he makes.
- **My sister** sends photos of the existing notebooks.
- **I** review imported entries initially and help set up the system.

The main experience is designed for my father, not for an administrator.

## What matters most

1. **Simple to use:** My father can use the main screen without reading or typing.
2. **Natural conversation:** The assistant asks useful questions without turning a chat into a form.
3. **Correct customer:** It does not guess which person a payment belongs to.
4. **Permission before change:** Every financial write or correction is connected to a real, explicit confirmation of that exact change.
5. **Complete history:** Old records and corrections remain available; balances come from the recorded history.
6. **Honest answers:** If information is missing or unclear, Sajelly says so and asks rather than inventing an answer.
7. **Private records:** Only authorized people can access the workshop's financial information.

## The first small release

We do not need to build every feature at once. Our first working test is intentionally small:

**Given a few verified customer records, my father can open Sajelly on Android, tap the microphone, ask in Egyptian Arabic how much someone owes, and hear the correct balance.** If a name is ambiguous, Sajelly asks which customer he means.

This first test is complete when it works on a real phone and its answers match the known records. We can put those first records in manually for the test.

After that, we can add the confirmed writing of purchases and payments, corrections, and the photo-import flow as small, separately tested pieces.

## Not part of the first release

General expense tracking, inventory, invoices, taxes, product catalogs, offline operation, and a full accounting dashboard are outside the current scope. They should not make this small tool harder to build or use.

---

**The goal:** Build the helper I used to be for my father — someone who listens, asks when unsure, remembers the money correctly, and helps him find answers without needing to read a notebook.
