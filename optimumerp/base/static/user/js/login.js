jQuery(function() {
    const $usernameInput = $("#id_username");
    const $passwordInput = $("#id_password");
    const $bgDarkClass = $(".bg_dark");
    
    $usernameInput.on("focus", function() {
        $(this).css("background-color", $bgDarkClass.css("background-color"));
    })
})