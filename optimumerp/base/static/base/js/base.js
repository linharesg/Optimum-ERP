jQuery(function() {
    // Link ativo
    const currentLocation = location.pathname;
    const $menuItems = $(".nav-link");

    $.each($menuItems, (_, menu) => {
        const $menu = $(menu);

        if ($menu.attr("href") === currentLocation) {
            $menu.attr("class", "nav-link active");
        } else {
            $menu.attr("class", "nav-link link-light");
        }
    });

    // Habilitar os toats de notificação
    $(".toast").toast("show");

    // Navbar animation
    const $navbar = $("#navbar");
    const $menuIcons = $(".menu-icons");
    const $linkName = $(".link-name");

    $navbar.hover(function() {
        $(this).stop().animate({ width: '200px' }, 300) // Anima a largura para 150px ao passar o mouse
        $linkName.css("display", "flex");
        console.log($linkName.text())
    }, function() {
        $(this).stop().animate({ width: '80px' }, 300) // Anima a largura para 80px ao retirar o mouse
        $linkName.css("display", "none");
    });
});