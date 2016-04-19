// adapted from https://gist.github.com/marothstein/5736913
var swipeBuffer = "";
var swipeTimeout = null;
var TIMEOUT_DURATION = 100;
var BLINK_DURATION = 400;

var attachSwipe = function() {
  $('body').keypress(function(e) {
    keyPressed(e);
  });
};

var addKeyToSwipeBuffer = function(keyCode, keyChar) {
  if (swipeBuffer == null) {
    swipeBuffer = "";
  }
  swipeBuffer += keyChar;
};

var clearSwipeBuffer = function() {
  delete swipeBuffer;
  swipeBuffer = null;
};

var keyPressed = function(e) {
  addKeyToSwipeBuffer(e.keyCode, String.fromCharCode(e.keyCode).trim());

  if (swipeTimeout == null) {
    swipeTimeout = setTimeout("processSwipe()", TIMEOUT_DURATION);
  } else {
    clearTimeout(swipeTimeout);
    swipeTimeout = setTimeout("processSwipe()", TIMEOUT_DURATION);
  }
};

var processSwipe = function() {
  var swipeSplit = swipeBuffer.split('=');

  if (validate(swipeSplit[1], swipeSplit[2])) {
    $('#display-text').html('Valid card. Sending data');
    var data = {
      studentID: swipeSplit[1],
      name: swipeSplit[2],
      raw: swipeBuffer
    }

    $.ajax({
      type: "POST",
      url: '/card-reader',
      data: data,
      success: function() {
        $('#display-text').html('Successful. Swipe another card.');
        blink(1);
        console.log('saved.');
      },
      error: function() {
        $('#display-text').html('Couldn\'t save, please try again');
        blink(2);
      }
    });
  } else {
    $('#display-text').html('Couldn\'t read card');
    blink(2);
  }

  clearSwipeBuffer();
};

var validate = function(studentId, name) {
  if (/[0-9]/.test(studentId) && /[a-zA-Z\/\s]/.test(name)) {
    return true;
  }
  return false;
}

var blink = function(n) {
  if (n > 0) {
    var elem = $('#display-text');
    setTimeout(function () {
      elem.css('visibility', 'hidden');
      setTimeout(function() {
        elem.css('visibility', 'visible');
        blink(n - 1);
      }, BLINK_DURATION);
    }, BLINK_DURATION);
  }
}
