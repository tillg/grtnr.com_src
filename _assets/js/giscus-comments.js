document.addEventListener("DOMContentLoaded", async function () {
    const commentElements = document.querySelectorAll(".comment-count");

    // GitHub API request function
    async function fetchCommentCount(postPath) {
        const repo = "tillg/grtnr.com_2024"; // Your repo
        const discussionCategory = "Comments"; // Your Giscus discussion category

        const query = `
        {
            repository(owner: "tillg", name: "grtnr.com_2024") {
                discussions(first: 100, category: "${discussionCategory}") {
                    nodes {
                        title
                        url
                        comments {
                            totalCount
                        }
                    }
                }
            }
        }`;

        try {
            const response = await fetch("https://api.github.com/graphql", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "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"
                },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) throw new Error("GitHub API error");

            const result = await response.json();
            if (!result.data) return null;

            const discussions = result.data.repository.discussions.nodes;

            // Find the discussion that matches the post's URL
            const discussion = discussions.find(d => postPath.includes(d.title));

            return discussion ? discussion.comments.totalCount : 0;
        } catch (error) {
            console.error("Failed to fetch Giscus comment count:", error);
            return 0;
        }
    }

    // Loop through all comment placeholders and update them
    commentElements.forEach(async (el) => {
        const postPath = el.getAttribute("data-giscus-comments");
        const count = await fetchCommentCount(postPath);
        el.querySelector(".comment-num").textContent = count;
    });
});
