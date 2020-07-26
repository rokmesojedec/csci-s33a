// Using self invoking function to create variable scope  
(() => {

  // API Helper Object
  const api = {
    compose: "/emails",
    mailbox: {
      sent: "/emails/sent",
      inbox: "/emails/inbox",
      archive: "/emails/archive",
    },
    PUT: (id) => { return `/emails/${id}`; },
    GET: (id) => { return `/emails/${id}`; }
  };

  /**
   * Generates a DOM element with optional child elements and attributes. Function can be nested in itself
   * @param {string} tag - Tag name
   * @param {string|HTMLElement|string[]|HTMLElement[]} innerHTML - Elements appended inside of the created tag
   * @param {object} - Key value pairs for creating attributes of the root tag
   * @author Rok Mesojedec
   */
  const $ = (function () {
    // Private helper function, used to append a DOM element. If passed element is string then it's appended as Text node instead
    let appendChild = (root, element) => {
      if (typeof element === "string")
        root.append(document.createTextNode(element));
      else if (element instanceof HTMLElement)
        root.append(element);
    };

    return (tag, { innerHTML, attributes } = {}) => {
      // Tag should not be null
      if (tag === null || tag === undefined) throw new Error("tag cannot be null or undefined.");

      // Create element from tag. TODO: add check if passed string matches any HTML element
      let root = document.createElement(tag);

      // innerHTML will be children elements added to formerly created element.
      // If innerHTML is an array than process each element and add it as a Text node or a HTML element
      if (innerHTML != null) {
        if (Array.isArray(innerHTML)) {
          innerHTML.forEach(element => {
            appendChild(root, element);
          });
        } else appendChild(root, innerHTML);
      }

      // Attributes parameter should be a JSON. 
      // For each key-value pair in this object an attribute object filled with corresponding value
      // is created and added to root element
      if (attributes != null && typeof attributes == "object") {
        for (let key in attributes) {
          let attr = document.createAttribute(key);
            attr.value = attributes[key];
            root.setAttributeNode(attr);
        }
      }
      return root;
    };
  })();


  // Helper function for creating ajax calls. Wraps the native fetch function
  const ajax = (method, endpoint, requestInit, responseJSON = true) => {
    let options = { method: method };
    if (requestInit != null && typeof requestInit === "object") {
      Object.assign(options, requestInit);
    }
    return responseJSON ? fetch(endpoint, options).then(response => response.json()) : fetch(endpoint, options);
  };


  // Populated on DOM loaded, because we need to reference actual DOM elements
  const views = {};

  // Shows view matching the passed argument name and hides others
  const showView = (show) => {
    for (let view in views) views[view].style.display = show == view ? "block" : "none";
  };

  // Hides all views
  const hideViews = () => {
    for (let view in views) views[view].style.display = "none";
  };

  // Empties inner content of a DOM object
  const clearDOM = (el) => {
    while (el.firstChild) el.removeChild(el.firstChild);
  };

  document.addEventListener('DOMContentLoaded', function () {
    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => loadMailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => loadMailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => loadMailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => composeEmail() );

    // Fill the "views" constant with view DOM references 
    Object.assign(views, {
      emails: document.querySelector('#emails-view'),
      compose: document.querySelector('#compose-view'),
      email: document.querySelector('#email-view'),
    });

    // Add submit button click event, which 'sends' and e-mail
    document.querySelector('input[type="submit"]').onclick = (event) => {
      event.preventDefault();
      ajax("POST", api.compose, {
        body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
        })
      }).then(data => {
        loadMailbox("sent");
      }).catch((error) => {
        console.error('Error:', error);
      });
      return false;
    };

    // By default, load the inbox
    loadMailbox('inbox');
  });

  // Shows compose e-mail view.
  // Prefills it with reply data, if email_id is passed
  function composeEmail(email_id) {
    // Get composition fields DOM elements
    let recipientsInput = document.querySelector('#compose-recipients');
    let subjectInput = document.querySelector('#compose-subject');
    let bodyInput = document.querySelector('#compose-body');

    // Hide all views - this is necessary so that called view shows the fade-in animation
    hideViews();

    // If no email_id is provided, then we show clean compose e-mail form
    if (email_id === undefined) {
      views.compose.querySelector("h3").innerHTML = "New Email";
      // Clear out composition fields
      recipientsInput.value = '';
      subjectInput.value = '';
      bodyInput.value = '';
      // Show compose view and hide other views
      showView("compose");
      bodyInput.focus();
    } else {
      // Else prefill compose email form with reply email data
      ajax("GET", api.GET(email_id)).then(email => {
        views.compose.querySelector("h3").innerHTML = "Reply";
        let subject;

        // Add "Re: " to subject line if it doesn't contain it already
        if (email.subject.toLowerCase().indexOf("re:") === 0) subject = email.subject;
        else subject = `Re: ${email.subject}`;
        // Prefill composition fields with content from reply email
        recipientsInput.value = email.sender;
        subjectInput.value = subject;
        // adding line to delimit previous message from reply. Also appends timestamp when 
        // previous mail was sent and by whom it was sent. 
        bodyInput.value = `\n\n------------------------------------------------\n` +
          `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
      }).catch(error => { console.error(error); }).finally(() => {
        // Show compose view and hide other views
        showView("compose");
        bodyInput.focus();
      });
    }
  }


  // Fetches mailbox data and creates DOM elements from that data and finally it injects them in the website
  function loadMailbox(mailbox) {
    // Show the mailbox name
    views.emails.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    let isSentMailbox = mailbox === "sent";

    // Hide all views - this is necessary so that called view shows the fade-in animation
    hideViews();

    ajax("GET", api.mailbox[mailbox])
      .then(data => {
        // Fetched data should be a non 0 length array
        if (data !== undefined && Array.isArray(data) && data.length > 0) {
          // Fetched e-mails will be shown as a styled HTML unordered list
          let root = $("ul", { attributes: { class: "emails-list" } });
          data.forEach(email => {
            // The data-id attribute used used by the e-mail on click function to open the actual e-mail body view.
            let attr = { "data-id": email.id };
            // If e-mail is not read, add class which will highlight in gray
            if (!email.read) attr["class"] = "unread";

            // Create e-mail list item DOM elements
            let emailElement = $("li", {
              innerHTML: [
                $("strong", { innerHTML: isSentMailbox ? `To: ${email.recipients.join(", ")}` : email.sender }),
                $("p", { innerHTML: email.subject }),
                $("time", { innerHTML: email.timestamp })],
              attributes: attr
            });

            // Adds an on click event for former element 
            // Cannot use arrow function here, because I need access to "this" object
            emailElement.onclick = function() { loadEmail(this.dataset.id, !isSentMailbox); };
            root.append(emailElement);
          });
          views.emails.append(root);
        } else {
          views.emails.append("Nothing to show ...");
        }
      }).catch((error) => {
        console.error('Error:', error);
      }).finally(() => {
        // Show the mailbox and hide other views
        showView("emails");
      });
  }

  // Sends a PUT request to archive/unarchive the e-mail with passed id
  function archiveEmail(id, archived) {
    ajax("PUT", api.PUT(id), { body: JSON.stringify({ 'archived': !archived }) }, false)
      .then(() => { loadMailbox("inbox"); })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  function loadEmail(id, archivable) {
    // Hide all views - this is necessary so that called view shows the fade-in animation
    hideViews();

    // Get the e-mail
    ajax("GET", api.GET(id)).then(email => {
      // If e-mail is not marked "read", send a PUT request to mark it as "read"
      // this happens async, so we don't need to worry about the promise.
      // Content displayed after it won't be affected
      if (!email.read)
        ajax("PUT", api.PUT(id), { body: JSON.stringify({ 'read': true }) }, false)
          .catch((error) => { console.error('Error:', error); });

      // If email container contains any child elements, we remove them first, so we're presented with a blank slate 
      clearDOM(views.email);

      // Prepares HTML elements which will display the email
      let innerElements = [
        $("h2", { innerHTML: email.subject }),
        $("div", { innerHTML: [$("strong", { innerHTML: "From: " }), email.sender] }),
        $("div", { innerHTML: [$("strong", { innerHTML: "To: " }), email.recipients.join(", ")] }),
        $("div", { innerHTML: [$("strong", { innerHTML: "Date: " }), email.timestamp] }),
        $("div", { innerHTML: [email.body], attributes: { class: "email-body" } })
      ];

      // If "archivable" parameter is false
      // do not create archive button for current email
      if (archivable) {
        let archiveButton = $("button", {
          innerHTML: [email.archived ? "Unarchive" : "Archive"],
          attributes: { class: "btn btn-sm btn-outline-primary ml-1" }
        });
        archiveButton.addEventListener("click", () => { archiveEmail(email.id, email.archived); });
        innerElements.unshift(archiveButton);
      }

      // Create Reply button, add onclick event on it - which opens compose email view
      let replyButton = $("button", { innerHTML: ["Reply"], attributes: { class: "btn btn-sm btn-outline-primary " } });
      replyButton.addEventListener("click", () => { composeEmail(email.id); });
      innerElements.unshift(replyButton);
      
      // Prepare e-mail root DOM
      let root = $("div", {
        innerHTML: innerElements,
        attributes: { class: "email-content" }
      });

      // Inject e-mail DOM elements into view
      views.email.append(root);

    }).finally(() => {
      showView("email");
    }).catch((error) => {
      console.error('Error:', error);
    });
  }
})();