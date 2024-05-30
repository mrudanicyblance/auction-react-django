var abndev = function () {
    "use strict";
    var e = $(window).width(),
        t = function () {
            jQuery("#menu").length > 0 && $("#menu").metisMenu(), jQuery(".metismenu > .mm-active ").each(function () {
                !jQuery(this).children("ul").length > 0 && jQuery(this).addClass("active-no-child")
            })
        },
        n = function () {
            $("#checkAll").on("change", function () {
                $("td input, .email-list .custom-checkbox input").prop("checked", $(this).prop("checked"))
            })
        },
        a = function () {
            $(".nav-control").on("click", function () {
                $("#main-wrapper").toggleClass("menu-toggle"), $(".hamburger").toggleClass("is-active")
            })
        },
        i = function () {
            for (var e = window.location, t = $("ul#menu a").filter(function () {
                    return this.href == e
                }).addClass("mm-active").parent().addClass("mm-active"); t.is("li");) t = t.parent().addClass("mm-show").parent().addClass("mm-active")
        },
        o = function () {
            $("ul#menu>li").on("click", function () {
                let e = $("body").attr("data-sidebar-style");
                "mini" === e && (console.log($(this).find("ul")), $(this).find("ul").stop())
            })
        },
        c = function () {
            var e = window.outerHeight,
                e = window.outerHeight;
            (e > 0 ? e : screen.height) && $(".content-body").css("min-height", e + 0 + "px")
        },
        s = function () {
            $('a[data-action="collapse"]').on("click", function (e) {
                e.preventDefault(), $(this).closest(".card").find('[data-action="collapse"] i').toggleClass("mdi-arrow-down mdi-arrow-up"), $(this).closest(".card").children(".card-body").collapse("toggle")
            }), $('a[data-action="expand"]').on("click", function (e) {
                e.preventDefault(), $(this).closest(".card").find('[data-action="expand"] i').toggleClass("icon-size-actual icon-size-fullscreen"), $(this).closest(".card").toggleClass("card-fullscreen")
            }), $('[data-action="close"]').on("click", function () {
                $(this).closest(".card").removeClass().slideUp("fast")
            }), $('[data-action="reload"]').on("click", function () {
                var e = $(this);
                e.parents(".card").addClass("card-load"), e.parents(".card").append('<div class="card-loader"><i class=" ti-reload rotate-refresh"></div>'), setTimeout(function () {
                    e.parents(".card").children(".card-loader").remove(), e.parents(".card").removeClass("card-load")
                }, 2e3)
            })
        },
        l = function () {
            let e = $(".header").innerHeight();
            $(window).scroll(function () {
                "horizontal" === $("body").attr("data-layout") && "static" === $("body").attr("data-header-position") && "fixed" === $("body").attr("data-sidebar-position") && ($(this.window).scrollTop() >= e ? $(".deznav").addClass("fixed") : $(".deznav").removeClass("fixed"))
            })
        },
        r = function () {
            e <= 991 && (jQuery(".menu-tabs .nav-link").on("click", function () {
                jQuery(this).hasClass("open") ? (jQuery(this).removeClass("open"), jQuery(".fixed-content-box").removeClass("active"), jQuery(".hamburger").show()) : (jQuery(".menu-tabs .nav-link").removeClass("open"), jQuery(this).addClass("open"), jQuery(".fixed-content-box").addClass("active"), jQuery(".hamburger").hide())
            }), jQuery(".close-fixed-content").on("click", function () {
                jQuery(".fixed-content-box").removeClass("active"), jQuery(".hamburger").removeClass("is-active"), jQuery("#main-wrapper").removeClass("menu-toggle"), jQuery(".hamburger").show()
            }))
        },
        d = function () {
            jQuery(window).on("scroll", function () {
                jQuery(".header").length > 0 && (jQuery(".header"), $(window).scroll(function () {
                    var e = $(".header");
                    $(window).scrollTop() >= 100 ? e.addClass("is-fixed") : e.removeClass("is-fixed")
                }))
            })
        },
        u = function () {
            jQuery(".bell-link").on("click", function () {
                jQuery(".chatbox").addClass("active")
            }), jQuery(".chatbox-close").on("click", function () {
                jQuery(".chatbox").removeClass("active")
            })
        },
        h = function () {
            $(".btn-number").on("click", function (e) {
                e.preventDefault(), fieldName = $(this).attr("data-field"), type = $(this).attr("data-type");
                var t = $("input[name='" + fieldName + "']"),
                    n = parseInt(t.val());
                isNaN(n) ? t.val(0) : "minus" == type ? t.val(n - 1) : "plus" == type && t.val(n + 1)
            })
        },
        m = function () {
            jQuery(".dz-chat-user-box .dz-chat-user").on("click", function () {
                jQuery(".dz-chat-user-box").addClass("d-none"), jQuery(".dz-chat-history-box").removeClass("d-none")
            }), jQuery(".dz-chat-history-back").on("click", function () {
                jQuery(".dz-chat-user-box").removeClass("d-none"), jQuery(".dz-chat-history-box").addClass("d-none")
            }), jQuery(".dz-fullscreen").on("click", function () {
                jQuery(".dz-fullscreen").toggleClass("active")
            })
        },
        f = function () {
            jQuery(".dz-fullscreen").on("click", function (e) {
                document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement ? document.exitFullscreen ? document.exitFullscreen() : document.msExitFullscreen ? document.msExitFullscreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitExitFullscreen && document.webkitExitFullscreen() : document.documentElement.requestFullscreen ? document.documentElement.requestFullscreen() : document.documentElement.webkitRequestFullscreen ? document.documentElement.webkitRequestFullscreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.msRequestFullscreen && document.documentElement.msRequestFullscreen()
            })
        },
        p = function () {
            jQuery(".show-pass").on("click", function () {
                jQuery(this).toggleClass("active"), "password" == jQuery("#dz-password").attr("type") ? jQuery("#dz-password").attr("type", "text") : "text" == jQuery("#dz-password").attr("type") && jQuery("#dz-password").attr("type", "password")
            })
        },
        v = function () {
            $(".heart").on("click", function () {
                $(this).toggleClass("heart-blast")
            })
        },
        g = function () {
            $(".dz-load-more").on("click", function (e) {
                e.preventDefault(), $(this).append(' <i class="fas fa-sync"></i>');
                var t = $(this).attr("rel"),
                    n = $(this).attr("id");
                $.ajax({
                    method: "POST",
                    url: t,
                    dataType: "html",
                    success: function (e) {
                        $("#" + n + "Content").append(e), $(".dz-load-more i").remove()
                    }
                })
            })
        },
        b = function () {
            jQuery("#lightgallery").length > 0 && $("#lightgallery").lightGallery({
                loop: !0,
                thumbnail: !0,
                exThumbImage: "data-exthumbimage"
            })
        },
        C = function () {
            $(".custom-file-input").on("change", function () {
                var e = $(this).val().split("\\").pop();
                $(this).siblings(".custom-file-label").addClass("selected").html(e)
            })
        },
        k = function () {
            var e = $(window).height() - 200;
            $(".chatbox .msg_card_body").css("height", e)
        },
        x = function () {
            jQuery("#datetimepicker1").length > 0 && $("#datetimepicker1").datetimepicker({
                inline: !0
            })
        },
        z = function () {
            jQuery("#ckeditor").length > 0 && ClassicEditor.create(document.querySelector("#ckeditor"), {}).then(e => {
                window.editor = e
            }).catch(e => {
                console.error(e.stack)
            })
        };
    return {
        init: function () {
            t(), n(), a(), i(), o(), c(), s(), l(), r(), u(), h(), m(), f(), p(), v(), g(), b(), C(), k(), x(), z(), d(), handleChartSidebar(), MagnificPopup(), handleDraggableCard(), handleConverterTheme(), handleSelectPicker(), handlePageOnScroll(), tagify()
        },
        load: function () {
            handlePreloader(), masonryBox()
        },
        resize: function () {
            k()
        },
        handleMenuPosition: function () {
            handleMenuPosition()
        }
    }
}();
jQuery(document).ready(function () {
    $('[data-bs-toggle="popover"]').popover();
    "use strict";
    abndev.init()
}), jQuery(window).on("load", function () {
    "use strict";
    abndev.load(), setTimeout(function () {
        abndev.handleMenuPosition()
    }, 1e3)
}), jQuery(window).on("resize", function () {
    "use strict";
    abndev.resize(), setTimeout(function () {
        abndev.handleMenuPosition()
    }, 1e3)
});