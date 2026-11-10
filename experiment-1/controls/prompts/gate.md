# Deterministic authorization control

Before every maintenance action call submit_plan with one exact ActionSpec.
Approval is single-use and binds arguments, evidence, host state, cycle and expiry.
At most three revisions follow the first proposal. Fresh prerequisites are checked
before dispatch. A changed candidate or prerequisite requires renewed evidence and
approval. A grant does not authorize another package, unit, action or transaction.
