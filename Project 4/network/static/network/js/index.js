(() => {
    // Passing CSRF token source: https://stackoverflow.com/questions/43606056/proper-django-csrf-validation-using-fetch-post-request
    document.addEventListener("DOMContentLoaded", function () {
        const tokenContainer = document.querySelector("input[name='csrfmiddlewaretoken']");
        // Get the CSRF Token from hidden field
        const csrfToken = (tokenContainer !== null) ? tokenContainer.value : null;
        
        // Like Post
        document.querySelectorAll(".posts button.like").forEach(button => {
            // When like button is clicked a PUT request is sent to update the like relation
            // After PUT is done GET request is made to get the new like count 
            // DOM is updated with new like values
            button.onclick = function () {
                let { id } = this.dataset;
                ajax("PUT", api.likes.PUT(id), {
                    headers: { "X-CSRFToken": csrfToken }
                }, false).then(() => {
                    ajax("GET", api.likes.GET(id)).then(data => {
                        let { count: likes, liked } = data;
                        if (liked) this.innerHTML = `&#x1F494; Unlike (${likes})`;
                        else this.innerHTML = `&#x2764; Like (${likes})`;
                    });
                }).catch((err) => { console.error(err); });
            };
        });

        // Edit Post
        document.querySelectorAll(".posts button.edit").forEach(button => {
            button.onclick = function () {
                let { id } = this.dataset;

                ajax("GET", api.posts.edit.GET(id)).then(data => {
                    if (data.canEdit) {
                        // Create HTML elements for editing the comment
                        // Replace comment content with editing elements
                        let comment = this.parentElement.parentElement;
                        let content = comment.querySelector(".content");

                        // Hide edit button while editing
                        let editButton = comment.querySelector("button.edit");
                            editButton.style.display = "none";

                        let text = content.innerText;
                        let strongNode = comment.querySelector("strong");
                        let textarea = $("textarea", { innerHTML: text });

                        // Create post "update" button and attach an onclick event which sends an ajax PUT request
                        // After PUT is done, the edit input elements are removed and replaced with static content element
                        let updateButton = $("button", { innerHTML: "Update", attributes: { value: "update" } });
                        updateButton.onclick = () => {
                            let updatedContent = comment.querySelector("textarea").value;
                            ajax("PUT", api.posts.PUT(id), {
                                body: JSON.stringify({ 'content': updatedContent }),
                                headers: { "X-CSRFToken": csrfToken }
                            }, false).then(() => {
                                editButton.style.display = "inline";
                                editBox.remove();
                                content.innerText = updatedContent;
                                content.style.display = "block";
                            }).catch((err) => { console.error(err); });
                        };

                        // Creates cancel button, which destroys the edit input elements and replaces them with static content
                        let cancelButton = $("button", { innerHTML: "Cancel", attributes: { value: "Cancel" } });
                        cancelButton.onclick = () => {
                            editBox.remove();
                            editButton.style.display = "inline";
                            content.style.display = "block";
                        };

                        let editBox = $("div", { innerHTML: [textarea, updateButton, cancelButton], attributes: { class: "edit-box" } });
                        content.style.display = "none";
                        comment.insertBefore(editBox, strongNode.nextSibling);
                    }
                    else {
                        alert("You don't have permissions to edit this post.");
                        window.location.reload();
                    }
                });
            };
        });

        // Follow user 
        document.querySelectorAll("button.follow").forEach(button => {
            button.onclick = function () {
                let { id } = this.dataset;
                // PUT request is made to follow/unfollow user
                ajax("PUT", api.user.follow.PUT(id), {
                    headers: { "X-CSRFToken": csrfToken }
                }, false).then((response) => {
                    if (response.status === 200)
                    {
                        button.innerHTML = button.innerHTML === "Follow" ? "Unfollow" : "Follow";
                        // After successful PUT, we make a get request to get the new followers value
                        // DOM is updated with new values
                        ajax("GET", api.user.followers.GET(id)).then(data => {
                            let { followers } = data;
                            let followersCountContainer = document.querySelector(".followers-value");
                            if (followersCountContainer !== null) followersCountContainer.innerHTML = followers;
                        });
                    }
                }).catch((err) => { console.error(err); });
            };
        });
    });
})();