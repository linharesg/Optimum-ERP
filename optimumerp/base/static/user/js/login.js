jQuery(function() {
    const $inputPassword = $("#id_password")
    const $inputUsername = $("#id_username")
    const $btnPassword = $("#btnPassword")
    const $eyeIcon = $("#eyeIcon")

    $btnPassword.on("click", () => {
        if ($inputPassword.attr("type") === "password") {
            $eyeIcon.removeClass("bi bi-eye-slash")
            $eyeIcon.addClass("bi bi-eye")
            $inputPassword.attr("type", "text");
        } else {
            $eyeIcon.removeClass("bi bi-eye")
            $eyeIcon.addClass("bi bi-eye-slash")
            $inputPassword.attr("type", "password");
        }
    });

    if ($inputPassword.hasClass("is-invalid")) {
        $btnPassword.css("left", "205px")
    } else {
        $btnPassword.css("left", "227px")
    };
});