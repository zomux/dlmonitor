/*
Javascript for Deep Community.
*/

INIT_KEYWORDS = "Hot Tweets,Fresh Tweets,Hot Papers,Fresh Papers";

dlmonitor = {
    ajaxCount: 0,
    previewTimeout: null,
};

dlmonitor.getKeywords = function() {
    var keywords = Cookies.get('keywords');
    if (Cookies.get('keywords') == undefined) {
        keywords = INIT_KEYWORDS;
    }
    if (!keywords) {
        var kwList = [];
    } else {
        var kwList = keywords.split(",");
    }
    return kwList;
};

// This requires js-cookie
dlmonitor.addKeyword = function(w) {
    if (w == undefined || typeof(w) == "object" || !w) {
        w = $("#new-keyword").val()
    }
    if (w.length == 0) {
        return;
    }
    if (w.includes(",")) {
        alert("Keyword can not include comma.");
        return;
    }
    if (w.length > 80) {
        alert("Keyword can not longer than 80 chars.")
        return;
    }
    $("#new-keyword").val("")
    var kwList = dlmonitor.getKeywords();
    if (kwList.length > 10) {
        alert("No more than 10 keywords, please.");
        return;
    }
    kwList.push(w.trim());
    var newKeywords = kwList.join(",");
    Cookies.set("keywords", newKeywords);
    // dlmonitor.showKeywords();
    dlmonitor.switchPreview(false);
    dlmonitor.updateAll();
};

dlmonitor.moveKeyword = function(e, dir) {
    var kwList = dlmonitor.getKeywords();
    var pos = $(e).data('pos');
    if ((pos == 0 && dir < 0) || (pos >= kwList.length - 1 && dir > 0)) {
        return;
    }
    var swapIdx = pos + dir;
    var swap = kwList[swapIdx];
    kwList[swapIdx] = kwList[pos];
    kwList[pos] = swap;
    console.log(pos,dir);
    var newKeywords = kwList.join(",");
    Cookies.set("keywords", newKeywords);
    dlmonitor.updateAll();
};

dlmonitor.removeKeyword = function(e) {
    var w = $(e).data('keyword');
    if (w == undefined) {
        return;
    }
    var kwList = dlmonitor.getKeywords();
    var index = kwList.indexOf(w);
    if (index > -1) {
        kwList.splice(index, 1);
    }
    var newKeywords = kwList.join(",");
    Cookies.set("keywords", newKeywords);
    dlmonitor.showKeywords();
    dlmonitor.updateAll();
};

// Deprecated
dlmonitor.showKeywords = function() {
    var newHtml = "";
    var kwList = dlmonitor.getKeywords();
    kwList.forEach(function(kw){
        newHtml += '<span class="label label-success" onclick="dlmonitor.removeKeyword(this);">' + kw + '</span>';
    });
    $("#keywords").html(newHtml);
};

dlmonitor.fetch = function(src_name, keyword, index, start) {
    if (start == undefined) start = 0;
    console.log("fetch", src_name, keyword, index, start);
    $("#posts-" + index).html(
        "<div style='text-align:center;'>"+
        "<img src='https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/0.16.1/images/loader-large.gif'/>"+
        "</div>");
    dlmonitor.ajaxCount ++;
    $.ajax({
       url: '/fetch',
       type: 'POST',
       data: {
          src: src_name,
          start: "" + start,
          keyword: keyword
       },
       error: function() {
           dlmonitor.ajaxCount --;
           alert("Error when fetching data.");
       },
       success: function(data) {
          // console.log(data);
          dlmonitor.ajaxCount --;
          $("#posts-" + index).html(data);
       }
    });
};

dlmonitor.convertDateInfo = function(token) {
    var dateinfo = "Recent two weeks";
    switch (token) {
        case '1-week':
            dateinfo = "Recent one week";
            break;
        case '2-week':
            dateinfo = "Recent two weeks";
            break;
        case '1-month':
            dateinfo = "Recent one month";
            break;
    }
    return dateinfo;
};

dlmonitor.showDate = function() {
    var datetoken = Cookies.get('datetoken');
    if (!datetoken) {
        datetoken = '2-week';
    }
    $("#date-info").html(dlmonitor.convertDateInfo(datetoken));
};

dlmonitor.filterDate = function(token) {
    Cookies.set('datetoken', token);
    dlmonitor.updateAll();
};

dlmonitor.placeColumns = function() {
    var kwList = dlmonitor.getKeywords();
    var currentNum = $(".post-columns .column").length
    // Create columns
    if (kwList.length != currentNum) {
        var newHtml = "";
        for (var i = 0; i < kwList.length; ++i) {
            var template = $("#column-template").html()
            for (var j = 0; j < 6; ++j) {
                template = template.replace("NUM", "" + i);
            }
            newHtml += template;
        }
        $("#post-columns").html(newHtml);
    }
    // Fill titles
    for (var i = 0; i < kwList.length; ++i) {
        $("#column-title-" + i).html(kwList[i]);
        $("#close-btn-" + i).data("keyword", kwList[i])
        $("#left-btn-" + i).data("pos", i)
        $("#right-btn-" + i).data("pos", i)
    }
};

// Deprecated
dlmonitor.fixFloat = function() {
    if (dlmonitor.ajaxCount != 0) return;
    var threshold = $("#post-columns").position().left + 1200 / 2;
    $(".post-columns .column").each(function(i, e) {
        if ($(e).position().left > threshold) {
            $(e).css("float", "right");
        }
    });
};

dlmonitor.updateAll = function(nofetch) {
    dlmonitor.showDate();
    dlmonitor.placeColumns();
    if (nofetch == true) return;
    var kwList = dlmonitor.getKeywords();
    for (var i = 0; i < kwList.length; ++i) {
        if (kwList[i].toLowerCase().includes("tweets")) {
            var src = 'twitter';
        } else {
            var src = 'arxiv';
        }
        dlmonitor.fetch(src, kwList[i], i, start=0);
    }
};

dlmonitor.switchPreview = function(flag) {
    if (flag) {
        $(".preview").show();
        $(".post-columns").hide();
    } else {
        $(".preview").hide();
        $(".post-columns").show();
    }
};

dlmonitor.init = function() {
    dlmonitor.updateAll(true);
    $("#new-keyword-btn").on('click tap', dlmonitor.addKeyword);
    $('#new-keyword').keypress(function(e) {
     var key = e.which;
     if(key == 13)  // the enter key code
      {
        $('#new-keyword-btn').click();
        return false;
      }
    });
    $('#new-keyword').on('keyup', function() {
        clearTimeout(dlmonitor.previewTimeout);
        dlmonitor.previewTimeout = setTimeout(function() {
            var text = $("#new-keyword").val();
            if ($("#new-keyword").is(":focus") && text.length >= 3) {
                $("#preview-kw").html(text);
                dlmonitor.switchPreview(true);
                dlmonitor.fetch('arxiv', text, 'preview');
            } else {
                dlmonitor.switchPreview(false);
            }
        }, 200);
        if ($("#new-keyword").val().length < 3) {
            dlmonitor.switchPreview(false);
        }
    });
    $("#close-btn-preview").on('click tap', function() {
            dlmonitor.switchPreview(false);
            $("#new-keyword").val('');
    });
};
