//--------------------------------------------------------------------------------------------------------------

var delay = (function() {
    var timer = 0;
    return function(callback, ms) {
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    };
})();


//--------------------------------------------------------------------------------------------------------------
var selection = '';
var flickrUser = '';
var tweet = {

    //----------------------------------------------------------------------------------------------------------
    init : function() {
        $("#tweet-main").keyup(function() {
            tweet.updateCount();
            tweet.getSearchTerm();
        }).mouseup(function() {
            tweet.getSearchTerm();
        }).select(function() {
            tweet.getSearchTerm();
        });

        $("#tweet-search").on("click", function() {
            tweet.getTagsAndImages();
            return false;
        });

        $("#location-update").on("click", function() {
            tweet.getLocation();
            return false;
        });

        $('#flickr-update').on("click", function() {
            tweet.getUserImages();
            return false;
        });

        $('.tab').click(function() {
           $(this).siblings('.tab-body').hide();
           $(this).siblings('.tab').removeClass('active');
           $(this).addClass('active');
           $($(this).attr('data-target')).show();
        });

        document.addEventListener("touchend", tweet.getSearchTerm, false);

        $("#tweet-post").click(function() {
            tweet.updateStatus();
            return false;
        })

        $("#tweet-main").on("focus", function() {
            tweet.showTooltip();
        });

        tweet.seeTweets();
    },
    //----------------------------------------------------------------------------------------------------------
    showTooltip : function() {
        $("#tweet-tooltip").fadeIn(100);
        setTimeout(function() {
            $("#tweet-tooltip span").addClass("highlight");
        }, 500);
    },
    //----------------------------------------------------------------------------------------------------------
    showSearchtip: function() {
         $("#tweet-tooltip").fadeOut(100);
         $("#tweet-search").fadeIn(100);
    },
    //----------------------------------------------------------------------------------------------------------
    getSearchTerm: function() {
        var range = $("#tweet-main").getSelection();
        if(range.text) {
            $("#tweet-search span").text(range.text);
            tweet.showSearchtip();
        }
    },
    //----------------------------------------------------------------------------------------------------------
    getTagsAndImages : function() {
        $(".tab").css('display','inline-block');
        // Only fetch if selected text has changed and isn't empty
        var selectedText = $("#tweet-search span").text();
        if (selectedText && selectedText != selection) {
            selection = selectedText;
            tweet.tags();
            tweet.images();
        }
    },
    //----------------------------------------------------------------------------------------------------------
     getUserImages : function() {
        // Only fetch if selected user has changed and isn't empty
        currUser = $('#flickr-user').val();
        if (currUser !== "" && currUser !== flickrUser) {
            flickrUser = currUser;
            tweet.userImages();
        }
    },
    //----------------------------------------------------------------------------------------------------------
     getLocation : function() {
        if (navigator.geolocation) { // check that the functionality exists first
            tweet.location();
        }
    },
    //----------------------------------------------------------------------------------------------------------
    seeTweets : function() {
        $("#notification-image").mouseenter(function() {
            $("#tweets").show();
        }).mouseleave(function() {
            $("#tweets").hide();
        });
    },
    //----------------------------------------------------------------------------------------------------------
    tags : function(e) {
        $(".section-tags .loader").fadeIn(300);
        $.ajax({
            type: "GET",
            url: "/hashtags?q=" + encodeURIComponent(selection),
            contentType: "application/json",
            success: function(data) {
                $("#tweet-tags").empty();
                $.each(data, function() {
                    $('#tweet-tags').prepend('<a href="' + this[0] + '" class="item">' + this[0] + ' (' + this[1] + ')</a>');
                });
                $(".section-tags .loader").hide();
                $("#tweet-tags .item").each(function(i) {
                    var self = $(this);
                    setTimeout(function() {
                        self.fadeIn(100).css("display","block");
                    }, 100 * i);
                });
                tweet.tagsBehavior();
            },
            error: function(xhr, status, error) {
                $('#tweet-tags').prepend('error loading tags ');
                $(".section-tags .loader").fadeOut(300);
            }
        });
        return false;
    },
    //----------------------------------------------------------------------------------------------------------
    location : function(e) {
        navigator.geolocation.getCurrentPosition(function (position) {
            $(".section-tags .loader").fadeIn(300);
            $.ajax({
                type: "GET",
                url: "/hashtags?location=" + position['coords'].latitude + "," + position['coords'].longitude,
                contentType: "application/json",
                success: function(data) {
                    $('#location-form').hide();
                    $("#location-tags").empty();
                    $.each(data, function() {
                        $('#location-tags').prepend('<a href="' + this[0] + '" class="item">' + this[0] + ' (' + this[1] + ')</a>');
                    });
                    $(".section-tags .loader").hide();
                    $("#location-tags .item").each(function(i) {
                        var self = $(this);
                        setTimeout(function() {
                            self.fadeIn(100).css("display","block");
                        }, 100 * i);
                    });
                    tweet.tagsBehavior();
                },
                error: function(xhr, status, error) {
                    $('#location-tags').text('error loading tags');
                    $(".section-tags .loader").fadeOut(300);
                }
            });
        },
        function (error) {
            $('#location-tags').text(error.message);
        });
    },
    //----------------------------------------------------------------------------------------------------------
    tagsBehavior : function() {
        $(".hashtag a.item").unbind("click").bind("click", function() {
            self = $(this);
            tag = '#' + self.attr('href');
            if (!(self.hasClass('added'))) {
                self.animate({
                    opacity: 0.2
                }, 100)
                .addClass('added');
                newValue = $("#tweet-main").val() + ' ' + tag;
            } else {
                self.animate({
                    opacity: 1
                }, 100)
                .removeClass('added');
                newValue = $("#tweet-main").val().replace(tag, '');
            }
            $("#tweet-main").val(newValue);
            tweet.updateCount();
            return false;
        });
    },
    //----------------------------------------------------------------------------------------------------------
    images : function(e) {
        $(".section-images .loader").fadeIn(300);
        $.ajax({
            type: "GET",
            url: "/photos?tags=" + encodeURIComponent(selection),
            contentType: "application/json",
            success: function(data) {
                $("#tweet-images").empty();
                $.each(data, function() {
                    $('#tweet-images').prepend('<a href="' + this.full + '" class="item"><img src="' + this.thumb + '"></a>');
                });
                $(".section-images .loader").hide();
                $("#tweet-images .item").each(function(i) {
                    var self = $(this);
                    setTimeout(function() {
                        self.fadeIn(100);
                    }, 100 * i);
                });
                tweet.imagesBehavior();
            },
            error: function(xhr, status, error) {
                $('#tweet-images').prepend('error loading images ');
                $(".section-images .loader").fadeOut(300);
            }
        });
        return false;
    },
    //----------------------------------------------------------------------------------------------------------
    userImages : function(e) {
        $(".section-images .loader").fadeIn(300);
        $.ajax({
            type: "GET",
            url: "/photos?user=" + flickrUser,
            contentType: "application/json",
            success: function(data) {
                $("#flickr-images").empty();
                $.each(data, function() {
                   $('#flickr-images').prepend('<a href="' + this.full + '" class="item"><img src="' + this.thumb + '"></a>');
                });
                $(".section-images .loader").hide();
                $("#flickr-user-form").hide();
                $("#flickr-images .item").each(function(i) {
                    var self = $(this);
                    setTimeout(function() {
                        self.fadeIn(100);
                    }, 100 * i);
                });
                tweet.imagesBehavior();
            },
            error: function(xhr, status, error) {
                $('#tweet-images').prepend('error loading images ');
                $(".section-images .loader").fadeOut(300);
            }
        });
    },
    //----------------------------------------------------------------------------------------------------------
    imagesBehavior : function() {
        $(".image a.item:not(.bound)").addClass('bound').on({
            click: function(self) {
                self = $(this);
                link = self.attr("href");
                if (!(self.hasClass("added"))) {
                    self.animate({
                        opacity: 0.2
                    }, 100)
                    .addClass("added");
                    newValue = $("#tweet-main").val() + " " + link;
                } else {
                    self.animate({
                        opacity: 1
                    }, 100)
                    .removeClass("added");
                    newValue = $("#tweet-main").val().replace(link,"");
                }
                $("#tweet-main").val(newValue);
                tweet.updateCount();
                return false;
            },
            mouseenter: function(self) {
                self = $(this);
                if (!(self.hasClass("added"))) {
                    self.animate({
                        opacity: 0.5
                    }, 100);
                }
            },
            mouseleave: function(self) {
                self = $(this);
                if (!(self.hasClass("added"))) {
                    self.animate({
                        opacity: 1
                    }, 100);
                }
            }
        })
    },
    //----------------------------------------------------------------------------------------------------------
    updateCount : function() {
        characterCount = 140 - ($("#tweet-main").val().length);
        $("#tweet-character-count").text(characterCount);
        if (characterCount < 0) {
            $("#tweet-character-count").addClass("negative");
        } else {
            $("#tweet-character-count").removeClass("negative");
        }
    },
    //----------------------------------------------------------------------------------------------------------
    updateStatus : function() {
        $.ajax({
            type: "GET",
            url: "/update_status?m=" + encodeURIComponent($("#tweet-main").val()),
            contentType: "application/json",
            success: function(data) {
                if(data.success) {
                    $("#tweet-main").val('');
                    $(".item").remove();
                    var statusHref = 'https://twitter.com/' + data.username + '/status/' + data.id,
                        statusText = 'View on Twitter',
                        statusHeader = 'Tweet Successfully Posted!';
                    toastr.success('<a target="_blank" href="' + statusHref + '">' + statusText + '</a>', statusHeader)
                    // Delay is required here
                    setTimeout(function() {
                        tweet.updateTweets();
                    }, 3000);
                    tweet.updateCount();
                } else {
                    toastr.error(data.status, 'Oops, we couldn\'t post your tweet')
                }
            },
            error: function(xhr, status, error) {
                toastr.error(error, 'Oops, we couldn\'t post your tweet')
            }
        });
    },
    //----------------------------------------------------------------------------------------------------------
    updateTweets : function() {
        $.ajax({
            type: "GET",
            url: "/tweets",
            success: function(text) {
                $("#tweets-list").html(text);
            }
        });
    }
}

//--------------------------------------------------------------------------------------------------------------
$(document).ready(function() {
    tweet.init();
});