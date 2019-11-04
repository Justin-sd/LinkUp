
$(document).ready(function() {

  //signUpNav
  $("#signUpNav").animatedModal({
    modalTarget: 'signUpNavModal',
    animatedIn: 'lightSpeedIn',
    animatedOut: 'bounceOut',
    color: '#39BEB9',
    beforeOpen: function() {
      var children = $(".thumb");
      var index = 0;
      function addClassNextChild() {
        if (index == children.length) return;
        children.eq(index++).show().velocity("transition.slideRightIn", {
          opacity: 1,
          stagger: 450,
            defaultDuration: 100
        });
        window.setTimeout(addClassNextChild, 100);
      }
      addClassNextChild();
    },
    afterClose: function() {
      $(".thumb").hide();
    }
  });

    //loginNav
  $("#loginNav").animatedModal({
    modalTarget: 'loginNavModal',
    animatedIn: 'bounceInUp',
    animatedOut: 'bounceOutDown',
    color: '#39BEB9',
    beforeOpen: function() {
      var children = $(".thumb");
      var index = 0;
      function addClassNextChild() {
        if (index == children.length) return;
        children.eq(index++).show().velocity("transition.slideUpIn", {
          opacity: 1,
          stagger: 450,
          defaultDuration: 100
        });
        window.setTimeout(addClassNextChild, 100);
      }
      addClassNextChild();
    },
    afterClose: function() {
      $(".thumb").hide();
    }
  });

    //signUpNav
  $("#signUp").animatedModal({
    modalTarget: 'signUpModal',
    animatedIn: 'lightSpeedIn',
    animatedOut: 'bounceOut',
    color: '#39BEB9',
    beforeOpen: function() {
      var children = $(".thumb");
      var index = 0;
      function addClassNextChild() {
        if (index == children.length) return;
        children.eq(index++).show().velocity("transition.slideRightIn", {
          opacity: 1,
          stagger: 450,
            defaultDuration: 100
        });
        window.setTimeout(addClassNextChild, 100);
      }
      addClassNextChild();
    },
    afterClose: function() {
      $(".thumb").hide();
    }
  });

    //loginNav
  $("#login").animatedModal({
    modalTarget: 'loginModal',
    animatedIn: 'bounceInUp',
    animatedOut: 'bounceOutDown',
    color: '#39BEB9',
    beforeOpen: function() {
      var children = $(".thumb");
      var index = 0;
      function addClassNextChild() {
        if (index == children.length) return;
        children.eq(index++).show().velocity("transition.slideUpIn", {
          opacity: 1,
          stagger: 450,
          defaultDuration: 100
        });
        window.setTimeout(addClassNextChild, 100);
      }
      addClassNextChild();
    },
    afterClose: function() {
      $(".thumb").hide();
    }
  });



});// end document ready
