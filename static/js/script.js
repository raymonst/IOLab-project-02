//--------------------------------------------------------------------------------------------------------------

var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();


//--------------------------------------------------------------------------------------------------------------

var tweet = {
	
    init : function() {
    	tweet.tags();
    	tweet.images();
    	
    	$("#tweet-main").keyup(function() {
    		tweet.updateCount();
    		tweet.updateLink();
    	});
    },

    tags : function() {
    	$("#tweet-find-tags").on("click", function() {
    		$("#tweet-tags .loader").fadeIn(300);
	    	return false;
    	});
    	tweet.tagsBehavior();
	},
	
    tagsBehavior : function() {
	    $("#tweet-tags a").on({
		    click: function(self) {
		    	self = $(this);
		    	tag = self.text();
		    	if (!(self.hasClass("added"))) {
				    self.animate({
				    	opacity: 0.2
				    }, 100)
				    .addClass("added");			    	
				    newValue = $("#tweet-main").val() + " " + tag;
		    	} else {
				    self.animate({
				    	opacity: 1
				    }, 100)
				    .removeClass("added");			    	
				    newValue = $("#tweet-main").val().replace(tag,"");
		    	}
				$("#tweet-main").val(newValue);
				tweet.updateCount();
				tweet.updateLink();
			    return false;
		    }
		});
	},
	
    images : function() {
    	$("#tweet-find-images").on("click", function() {
    		$("#tweet-images .loader").fadeIn(300);
    		$.ajax({
	    		type: "GET",
	    		url: "http://jsonpify.heroku.com?resource=http://metatweet.herokuapp.com/photos?tags=halloween",
	    		contentType: "application/json",
	    		dataType: "jsonp",
	    		success: function(data) {
	    		    $.each(data, function() {
	    		    	$('#tweet-images').append('<a href="' + this.full + '" class="item"><img src="' + this.thumb + '"></a>');
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
	    		    $('#tweet-images').append('error loading images');
	    		    $("#tweet-images .loader").fadeOut(300);
	    		}
		    });
	    	$("#tweet-images").show();
	    	return false;
    	});
    	tweet.imagesBehavior();
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