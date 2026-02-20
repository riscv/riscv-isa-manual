module.exports = async ({ github, context, tagChanges }) => {
    const prNumber = context.payload.pull_request.number;

    const body = `## Normative Tag Changes (Approved)

This PR has the \`normative-change-approved\` label, so the check will pass despite detected changes.

<details>
<summary>View Changes</summary>

${tagChanges || 'No detailed changes available.'}

</details>`;

    await github.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: prNumber,
        body: body
    });
};
