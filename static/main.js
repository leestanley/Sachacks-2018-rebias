loadingFeed = false;
function loadFeed(template, category) {
  loadingFeed = true;

  $("#feed").empty();
  $.ajax({
    url: "./api/getNews",
    type: "GET",
    data: {
      category: category
    },
    dataType: "json",
    success: function(res) {
      $.each(res, function(index, data) {
        tempItm = $(template).clone();
        $("#title-article", $(tempItm)).text(data.title);
        $(tempItm).css("background-image", "url(" + data.image + ")");
        //$(".sample-content").html(data.content.substring(0, 500));
        $("#feed").append(tempItm);

        $(".readmore", $(tempItm)).click(function() {
          
        });

        $("#above_feed").show();
        $("#feed").show();
        $("html, body").animate({
          scrollTop: $("#above_feed").offset().top
        }, 500);
      });

      loadingFeed = false;
    }
  });
}

$(window).on('load', function() {
  $("#above_feed").hide();
  $("#feed").hide();
  clonedFeedItem = $(".news-container").clone();
  $("#feed").empty(); // clear out the items, we just needed it for a template.

  selectedCat = null;
  // grab the buttons within the "bOptions" div
  $("#bOptions").find("button").each(function(index, element) {
    $(element).click(function() {
      if (!loadingFeed) {
        selectedCat = $(element).text().trim().toLowerCase();
        loadFeed(clonedFeedItem, selectedCat);
      }
    });
  });
});

$(document).on({
  ajaxStart: function() {
    $("body").addClass("loading");
  },
  
  ajaxStop: function() {
    $("body").removeClass("loading");
  }
})