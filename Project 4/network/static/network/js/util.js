// API Helper Object
const api = {
    likes: {
        PUT: (id) => { return `/like/${id}`; },
        GET: (id) => { return `/like/${id}`; },
    },
    posts: {
        PUT: (id) => { return `/posts/${id}`; },
        edit: {
            GET: (id) => { return `/edit/${id}`; }
        }
    },
    user: {
        GET: (id) => { return `/user/${id}`; },
        follow: {
            PUT: (id) => { return `/user/${id}/follow`; }
        },
        followers: {
            GET: (id) => { return `/user/${id}/followers`; }
        }
    }
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
