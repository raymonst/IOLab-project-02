//--------------------------------------------------------------------------------------------------------------

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();


//--------------------------------------------------------------------------------------------------------------
var selection = '';

var tweet = {

    init : function() {
    	$("#tweet-main").keyup(function() {
    		tweet.updateCount();
    		tweet.updateLink();
    		tweet.getTagsAndImages();
    	}).mouseup(tweet.getTagsAndImages);
    },

    getTagsAndImages : function() {
        var range = $("#tweet-main").getSelection();
        if(range.text && range.text != selection) {
            selection = range.text;
            tweet.tags();
            tweet.images();
        }
    },

    tags : function(e) {
        $("#tweet-tags .loader").fadeIn(300);
        $.ajax({
    		type: "GET",
    		url: "/hashtags?q="+selection,
    		contentType: "application/json",
    		success: function(data) {
    		    $.each(data, function() {
    		    	$('#tweet-tags').prepend('<a href="' + this[0] + '" class="item">' + this[0] + ' (' + this[1] + ')</a><br />');
    		    });
    		    $("#tweet-tags .loader").hide();
    		    $("#tweet-tags .item").each(function(i) {
    		        var self = $(this);
    		        setTimeout(function() {
    		        	self.fadeIn(100);
    		        }, 100 * i);
    		    });
    		    tweet.tagsBehavior();
    		},
    		error: function(xhr, status, error) {
    		    $('#tweet-tags').prepend('error loading tags');
    		    $("#tweet-tags .loader").fadeOut(300);
    		}
        });
    	$("#tweet-tags").show();
    	return false;

    },

    tagsBehavior : function() {
	    $("#tweet-tags a").on({
		    click: function(self) {
		    	self = $(this);
		    	tag = self.attr('href');
		    	if (!(self.hasClass('added'))) {
				    self.animate({
				    	opacity: 0.2
				    }, 100)
				    .addClass('added');
				    newValue = $("#tweet-main").val() + ' #' + tag;
		    	} else {
				    self.animate({
				    	opacity: 1
				    }, 100)
				    .removeClass('added');
				    newValue = $("#tweet-main").val().replace(tag, '');
		    	}
				$("#tweet-main").val(newValue);
				tweet.updateCount();
				tweet.updateLink();
			    return false;
		    }
		});
	},

    images : function(e) {
	    $("#tweet-images .loader").fadeIn(300);
        $.ajax({
    		type: "GET",
    		url: "/photos?tags="+selection,
    		contentType: "application/json",
    		success: function(data) {
    		    $.each(data, function() {
    		    	$('#tweet-images').prepend('<a href="' + this.full + '" class="item"><img src="' + this.thumb + '"></a>');
    		    });
    		    $("#tweet-images .loader").hide();
    		    $("#tweet-images .item").each(function(i) {
    		        var self = $(this);
    		        setTimeout(function() {
    		        	self.fadeIn(100);
    		        }, 100 * i);
    		    });
    		    tweet.imagesBehavior();
    		},
    		error: function(xhr, status, error) {
    		    $('#tweet-images').prepend('error loading images');
    		    $("#tweet-images .loader").fadeOut(300);
    		}
	    });
    	$("#tweet-images").show();
    	return false;

    },

    imagesBehavior : function() {
	    $("#tweet-images a").on({
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
				tweet.updateLink();
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

    updateCount : function() {
    	characterCount = 140 - ($("#tweet-main").val().length);
	    $("#tweet-character-count").text(characterCount);
	    if (characterCount < 0) {
			$("#tweet-character-count").addClass("negative");
	    } else {
			$("#tweet-character-count").removeClass("negative");
	    }
    },

    updateLink : function() {
	    delay(function() {
	    	newLink = "https://twitter.com/intent/tweet?text=" + $("#tweet-main").val().replace(/#/g, "%23");
	        $("#tweet-post").attr("href", newLink);
	    }, 1000);
    }

}



//--------------------------------------------------------------------------------------------------------------

$(document).ready(function() {

	tweet.init();

});