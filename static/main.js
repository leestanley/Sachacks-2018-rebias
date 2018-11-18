loadingFeed = false;
function loadFeed(template, category, popupTemplate) {
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
        $(tempItm).attr("id", index);
        bodyP = $(".sample-content", $(tempItm));
        if (data.content) {
          bodyP.html(data.content);
        } else {
          bodyP.html("<b>Loading...</b>");
          $.ajax({
            url: "./api/scrapText",
            type: "GET",
            data: {
              articleUrl: data.url
            },
            success: function(content) {
              // somehow can't get it to work with jQuery so this is my way around the problem.
              document.getElementById(index.toString()).getElementsByClassName("sample-content")[0].innerHTML = content.substring(0, 600) + "...";
            }
          });
        }
        $("#feed").append(tempItm);

        $(".readmore", $(tempItm)).click(function() {
          popup = $(popupTemplate).clone();
          $(popup).attr("id", "p" + index.toString());
          $(".x", $(popup)).click(function() {
            $(popup).remove();
          });

          $("#title-article", $(popup)).text(data.title);
          bodyP = $(".long-content", $(popup));
          bodyP.html(""); // default for now

          $("#userRating").on("change", function(e) {
            val = $("#userRating").val();

            $("#rating_label").text("Your rating on this article: " + val);
          });

          $("body").append(popup);
          $(popup).css("visibility", "visible");

          if (data.content) {
            bodyP.html(data.content);
          } else {
            bodyP.html("<b>Loading...</b>");
            $.ajax({
              url: "./api/scrapText",
              type: "GET",
              data: {
                articleUrl: data.url
              },
              success: function(content) {
                // somehow can't get it to work with jQuery so this is my way around the problem.
                document.getElementById("p" + index.toString()).getElementsByClassName("long-content")[0].innerHTML = content;
              }
            });
          }
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
  clonedPopup = $(".popup-content").clone();
  $("#feed").empty(); // clear out the items, we just needed it for a template.

  selectedCat = null;
  // grab the buttons within the "bOptions" div
  $("#bOptions").find("button").each(function(index, element) {
    $(element).click(function() {
      if (!loadingFeed) {
        selectedCat = $(element).text().trim().toLowerCase();
        loadFeed(clonedFeedItem, selectedCat, clonedPopup);
      }
    });
  });

  $(".popup-content").remove();
});