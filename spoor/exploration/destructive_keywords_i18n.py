"""Non-English destructive-action keyword sets (ROADMAP.md §2e, closes #101).

`spoor/exploration/safety.py`'s destructive-action guard matched English keywords
only — a UI labeled in another language wasn't recognized as destructive at all,
silently narrowing the §2e non-negotiable (sandbox-only destructive actions) to
English-labeled sites. Rather than detecting a target's language (no such
mechanism exists in this codebase, and guessing wrong is its own risk), the guard
always matches against the union of every language's keywords here *and* the
existing English set, unconditionally — no locale to declare or detect. A false
positive here (treating a safe label as destructive) only ever costs a skipped,
revisitable action; a false negative costs a real destructive action firing on a
real site. Over-matching is the safe direction, so there is no reason to pick just
one language's list.

Each set mirrors the same semantic list `DESTRUCTIVE_KEYWORDS` documents in
English: delete, remove, buy/purchase, pay, confirm, send, submit payment, log
out, place/cancel/return order. Translations are common, idiomatic UI verb forms
(infinitive or imperative, as typically rendered on a button/link), not a literal
word-for-word gloss — matched the same whole-word, case-insensitive way as English.

Covers only space-delimited languages, by design: the matcher is a `\\b`-bounded
regex, which relies on whitespace/punctuation word boundaries that languages
written without spaces between words (Chinese, Japanese, Thai, ...) don't have, so
extending to those needs a tokenizer, not just a longer keyword list — tracked as
a separate, not-yet-designed follow-up (ROADMAP.md §9) rather than silently
mismatching here.
"""

from __future__ import annotations

#: Spanish.
KEYWORDS_ES = frozenset(
    {
        "eliminar",
        "borrar",
        "quitar",
        "comprar",
        "pagar",
        "confirmar",
        "enviar",
        "enviar pago",
        "cerrar sesión",
        "realizar pedido",
        "hacer pedido",
        "cancelar pedido",
        "devolver pedido",
    }
)

#: German.
KEYWORDS_DE = frozenset(
    {
        "löschen",
        "entfernen",
        "kaufen",
        "bezahlen",
        "zahlen",
        "bestätigen",
        "senden",
        "zahlung senden",
        "abmelden",
        "ausloggen",
        "bestellung aufgeben",
        "bestellung stornieren",
        "bestellung zurücksenden",
    }
)

#: French.
KEYWORDS_FR = frozenset(
    {
        "supprimer",
        "retirer",
        "enlever",
        "acheter",
        "payer",
        "confirmer",
        "envoyer",
        "envoyer le paiement",
        "se déconnecter",
        "déconnexion",
        "passer la commande",
        "annuler la commande",
        "retourner la commande",
    }
)

#: Portuguese.
KEYWORDS_PT = frozenset(
    {
        "excluir",
        "apagar",
        "remover",
        "comprar",
        "pagar",
        "confirmar",
        "enviar",
        "enviar pagamento",
        "sair",
        "encerrar sessão",
        "fazer pedido",
        "cancelar pedido",
        "devolver pedido",
    }
)

#: Italian.
KEYWORDS_IT = frozenset(
    {
        "eliminare",
        "elimina",
        "cancellare",
        "rimuovere",
        "comprare",
        "acquistare",
        "pagare",
        "confermare",
        "inviare",
        "invia pagamento",
        "disconnetti",
        "esci",
        "effettua ordine",
        "annulla ordine",
        "restituisci ordine",
    }
)

#: Dutch.
KEYWORDS_NL = frozenset(
    {
        "verwijderen",
        "kopen",
        "betalen",
        "bevestigen",
        "verzenden",
        "versturen",
        "betaling verzenden",
        "uitloggen",
        "afmelden",
        "bestelling plaatsen",
        "bestelling annuleren",
        "bestelling retourneren",
    }
)

#: Every non-English set above, unioned — what `safety.py` adds to its own
#: English `DESTRUCTIVE_KEYWORDS` to build the single matched-against set.
ALL_I18N_KEYWORDS = frozenset().union(
    KEYWORDS_ES, KEYWORDS_DE, KEYWORDS_FR, KEYWORDS_PT, KEYWORDS_IT, KEYWORDS_NL
)
