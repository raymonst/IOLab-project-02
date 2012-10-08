//--------------------------------------------------------------------------------------------------------------

var tweet = {
	
    init : function() {
    	tweet.tags();
    	tweet.images();
    	tweet.post();
    },

    tags : function() {
    	$("#tweet-find-tags").on("click", function() {
	    	$("#tweet-tags").show();
	    	return false;
    	});
	    $("#tweet-tags a").on("click", function(self) {
		    self = $(this);
		    newValue = $("#tweet-main").val() + " " + self.text();
		    $("#tweet-main").val(newValue);
		    self.animate({
		    	opacity: 0.5
		    }, 500);
		    return false;
	    });
    },

    images : function() {
    	$("#tweet-find-images").on("click", function() {
    		$.ajax({
	    		type: "GET",
	    		url: "http://metatweet.herokuapp.com/photos?tags=halloween",
	    		contentType: "application/json",
	    		dataType: "jsonp",
	    		success: function(data) {
	    			alert("success");
	    		    $.each(data, function() {
	    		    	$('#tweet-images').append(this.thumb);
	    		    });	
	    		},
	    		error: function(xhr, status, error) {
	    		}

		    });
	    	$("#tweet-images").show();
	    	return false;
    	});
	    $("#tweet-images a").on("click", function(self) {
		    self = $(this);
		    newValue = $("#tweet-main").val() + " " + self.text();
		    $("#tweet-main").val(newValue);
		    self.animate({
		    	opacity: 0.5
		    }, 500);
		    return false;
	    });
    },

    post : function() {
    	$("#tweet-post").on("click", function() {
	    	console.log("test");
		    return false;
    	});
    }
	
}



//--------------------------------------------------------------------------------------------------------------

$(document).ready(function() {

	tweet.init();

});