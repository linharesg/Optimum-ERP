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
    const $linkName = $(".link-name");
    const $titlebar = $(".titlebar");
 
    $navbar.hover(function() {
        $(this).stop().animate({ width: '200px' }, 300) // Anima a largura para 150px ao passar o mouse
        $titlebar.stop().animate({ width: 'calc(100vmax - 205px)'}, 300)
        $linkName.fadeIn(300);
        $linkName.css({
            "display": "inline-block",
        });
    }, function() {
        $(this).stop().animate({ width: '80px' }, 300) // Anima a largura para 80px ao retirar o mouse
        $titlebar.stop().animate({ width: 'calc(100vmax - 85px)'}, 300)
        $linkName.fadeOut(300);
    });
});