function updateBar(value) {
  $("#pbar").attr("aria-valuenow", value);
  $("#pbar").html(value.toString() + "%");

  color = "";
  if (value == 50) {
    color = "#f39c12 !important";
  } else if (value > 50) {
    color = "#95a5a6 !important";
  } else if (value < 50) {
    color = "#3498db !important";
  }

  $("#pbar").css("background-color", color);
  $("#pbar").css("width", value.toString() + "%");
}

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
        //if (data.content) {
        //  bodyP.html(data.content);
        //} else {
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
        //}
        $("#feed").append(tempItm);

        // switch (category) {
        //   case "technology":
        //     $(".welcome-parallax").css("background-image", "url(codingpara.jpg)");
        //     break;
        //   case "politics":
        //     $(".welcome-parallax").css("background-image", "url(background.jpg)");
        //     break;
        //   case "economy":
        //     $(".welcome-parallax").css("background-image", "url(econ.jpg)");
        //     break;
        //   case "sports":
        //     $(".welcome-parallax").css("background-image", "url(econpara.jpg)");
        //     break;
        // }

        $("footer").css("visibility", "visible");

        $(".readmore", $(tempItm)).click(function() {
          popup = $(popupTemplate).clone();
          $(popup).attr("id", "p" + index.toString());
          $(".x", $(popup)).click(function() {
            $(popup).remove();
          });

          $("#title-article", $(popup)).text(data.title);
          bodyP = $(".long-content", $(popup));
          bodyP.html(""); // default for now

          $("body").append(popup);
          $(popup).css("visibility", "visible");

          slider = document.getElementById("userRating");
          slider.addEventListener("input", function() {
            $("#rating_label").text("Your rating on this article: " + slider.value);
          });

          $(".submit-btn", $(popup)).click(function() {
            $.ajax({
              url: "./api/updateWeight",
              type: "GET",
              data: {
                url: data.url,
                source: data.id,
                user_rating: slider.value
              },
              success: function(content) {
                updateBar(parseInt(content));
                $(popup).remove();
                loadFeed(template, category, popupTemplate);
              }
            });
          });

          //if (data.content) {
          //  bodyP.html(data.content);
          //} else {
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
          //}
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

  $.ajax({
    url: "./api/getWeight",
    type: "GET",
    success: function(weight) {
      updateBar(parseInt(weight));
    }
  });
});