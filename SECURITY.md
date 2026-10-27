# Security policy

This repository publishes explicitly approved public static demonstrations only.
Never commit client briefs, customer data, contracts, credentials or private source.
Keep each client's confidential application and storage separate from this origin.

Before release, review the exact revision and publication allowlist, pass the
validate check and confirm the full main SHA through the manual release workflow.
Repository administrators must separately enforce branch and environment rules.
An empty required-review count permits self-merge; independent review requires a
named second maintainer and must not be claimed until configured and verified.

If a credential is exposed, revoke it immediately. Removing the file is not
enough. Preserve restricted incident evidence and check deployments and history.
Do not disclose secrets or personal data in public issues or workflow logs.
Report privately to the project owner through the established client channel;
no new reporting email or service is implied by this document.

Checks are defense in depth, not a guarantee. Gitleaks does not cover every
secret format or personal information. The allowlist restricts paths rather than
business sensitivity. Pages is not a production ecommerce or payment platform.
