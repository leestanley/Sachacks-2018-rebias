loadingFeed = false;
function loadFeed(template, category) {
  loadingFeed = true;

  $("body").addClass("loading");
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
        if (data.content) {
          $(".sample-content", $(tempItm)).html(data.content);
        } else {
          $(".sample-content", $(tempItm)).html("<b>Loading...</b>");

          $.ajax({
            url: "./api/scrapText",
            type: "GET",
            data: {
              articleUrl: data.url
            },
            success: function(text) {
              console.log(text);
              $(".sample-content", $(tempItm)).html(text.substring(0, 100) + "...");
            }
          });
        }
        $("#feed").append(tempItm);

        $(".readmore", $(tempItm)).click(function() {
          console.log(data.url);
        });

        $("#above_feed").show();
        $("#feed").show();
        $("html, body").animate({
          scrollTop: $("#above_feed").offset().top
        }, 500);
      });

      $("body").removeClass("loading");
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