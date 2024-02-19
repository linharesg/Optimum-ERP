jQuery(function() {
    const $enabledCheckbox = $(".form-check-input")

    $enabledCheckbox.on("click", function(){
        const url = $(this).data("url")
        const isChecked = $(this).prop("checked"); // Get the original state of the checkbox

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": Cookies.get("csrftoken")
            }
        })
        .then(res => {
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json();
        })
        .then(data => {
            console.log(data);
            // Update checkbox status based on the response
            if (data.message === "error") {
                $(this).prop("checked", !isChecked); // Toggle checkbox state
                location.reload()
            } else {
                // Restore original checkbox state if validation fails
                $(this).prop("checked", isChecked);
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            // Restore original checkbox state if an error occurs
            $(this).prop("checked", isChecked);
        });
    })
})
