function update_data() 
{
   $SCRIPT_ROOT = window.location.origin;
   $.getJSON($SCRIPT_ROOT+"/_data",
      function(data) 
      {
         $("#temperature").text(data.temperature);
         $("#humidity").text(data.humidity);
      }
   );
}

setInterval(update_data, 10000);
window.onload = update_data;
