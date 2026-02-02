module.exports = async ({ github, context, tagChanges }) => {
    const owner = context.repo.owner;
    const repo = context.repo.repo;
    const labels = ['NormRules', 'Script Generated'];

    // This script only handles push events (merge to main)
    const commitSha = context.sha;
    const shortSha = commitSha.substring(0, 7);
    const commitUrl = `${context.payload.repository.html_url}/commit/${commitSha}`;
    const pusher = context.payload.pusher?.name || context.actor;

    const issueTitle = `Normative rule changes detected in commit ${shortSha}`;

    const issueBody = `## Normative Rule Changes Detected

The normative tag validation has detected changes after merge to main.

**Commit Details:**
- **SHA:** \`${shortSha}\`
- **Pushed by:** @${pusher}
- **Link:** ${commitUrl}

---

${tagChanges || 'No detailed changes available.'}

---

**Action Required:**
1. Review the normative rule changes in this commit
2. Verify that the changes are intentional and properly documented
3. If modifications or deletions need to be addressed, coordinate with the PR author or create a follow-up PR

> **Note:** Reference files have been automatically updated for any new tag additions. This issue is for tracking modifications and deletions that may require CSC review.

cc: @riscv/csc

*This issue was automatically created by the normative tag check workflow.*`;

    // Check if an issue already exists for this commit
    const existingIssues = await github.rest.issues.listForRepo({
        owner,
        repo,
        labels: labels.join(','),
        state: 'open'
    });

    const existingIssue = existingIssues.data.find(issue =>
        issue.title.includes(shortSha)
    );

    if (existingIssue) {
        console.log(`Issue already exists for this commit: ${existingIssue.html_url}`);
    } else {
        // Create a new issue
        const newIssue = await github.rest.issues.create({
            owner,
            repo,
            title: issueTitle,
            body: issueBody,
            labels
        });

        console.log(`Created issue: ${newIssue.data.html_url}`);
    }
};
