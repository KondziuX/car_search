document.addEventListener('DOMContentLoaded', function(){
        var currentStep = 1;
        var maxStep = 4;
    
        $(".nextBtn").click(function () {
          if (currentStep < maxStep) {
            $(".step-" + currentStep).addClass("d-none");
            currentStep++;
            $(".step-" + currentStep).removeClass("d-none");
            updateProgressBar();
          }
        });
    
        $(".prevBtn").click(function () {
          if (currentStep > 1) {
            $(".step-" + currentStep).addClass("d-none");
            currentStep--;
            $(".step-" + currentStep).removeClass("d-none");
            updateProgressBar();
          }
        });
    
        function updateProgressBar() {
          var progress = (currentStep - 1) * (75 / 3);
          $(".progress-bar").css("width", progress + "%").attr("aria-valuenow", progress).text(progress + "%");
    
          if (currentStep === 1) {
            $(".prevBtn").hide();
          } else {
            $(".prevBtn").show();
          }
    
          if (currentStep === maxStep) {
            $(".nextBtn").hide();
            $(".submitBtn").show();
          } else {
            $(".nextBtn").show();
            $(".submitBtn").hide();
          }
    
          updatePoints();
        }
    
        function updatePoints() {
          var points = 0;
          var totalFields = 36;
          var totalImages = 8;
    
          // Calculate points for fields (2 points each)
          $('form .form-control').each(function () {
            if ($(this).val()) {
              points += 2;
            }
          });
    
          // Calculate points for images (2 points each)
          $('form .form-control-file').each(function () {
            if ($(this).val()) {
              points += 2;
            }
          });
    
          // Calculate points for description (8 points)
          if ($('#description').val().trim().length > 0) {
            points += 8;
          }
    
          // Update spinner color and text
          var pointsText = $('#pointsText');
          pointsText.text(points + ' pkt.');
    
          // Update SVG circle progress
          var progressCircle = $('#progressCircle');
          var radius = 45;
          var circumference = 2 * Math.PI * radius;
          var offset = circumference - (points / 100 * circumference);
          progressCircle.css('stroke-dashoffset', offset);
    
          // Change spinner color based on points
          if (points >= 90) {
            progressCircle.attr('stroke', 'green');
          } else if (points >= 50) {
            progressCircle.attr('stroke', 'orange');
          } else {
            progressCircle.attr('stroke', 'red');
          }
        }
    
        $('form .form-control, form .form-control-file, #description').on('change input', function () {
          updatePoints();
        });
    
        updateProgressBar();
        updatePoints();
});