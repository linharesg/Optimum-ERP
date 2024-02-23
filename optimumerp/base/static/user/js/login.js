jQuery(function() {
    const $inputPassword = $("#id_password")
    const $btnPassword = $("#btnPassword")
    const $eyeIcon = $("#eyeIcon")

    $btnPassword.on("click", () => {
        if ($inputPassword.attr("type") === "password") {
            $eyeIcon.removeClass("bi bi-eye-slash")
            $eyeIcon.addClass("bi bi-eye")
            $inputPassword.attr("type", "text");
            console.log("teste")
        } else {
            $eyeIcon.removeClass("bi bi-eye")
            $eyeIcon.addClass("bi bi-eye-slash")
            $inputPassword.attr("type", "password");
        }
    });
});