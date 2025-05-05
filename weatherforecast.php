<!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Forecast Weather using PHP</title>
    <style>
        .report-container {
            border: #E0E0E0 1px solid;
            padding: 20px 40px 40px 40px;
            border-radius: 2px;
            margin: 0 auto;
            color: #929292;
        }
        .weather-icon {
            vertical-align: middle;
            margin-right: 20px;
        }
        .weather-forecast {
            color: #212121;
            font-size: 1.2em;
            font-weight: bold;
            margin: 20px 0px;
        }
        span.min-temperature {
            margin-left: 15px;
            color: #929292;
        }
        .time {
            line-height: 25px;
        }
    </style>
</head>
<body>
<div class="report-container">
    <?php
    // put your code here
    $currentTime = time();


    // Create a function called getForecast that accepts a city as a parameter and returns an array with the
    // the weather description, icon, maxtemp, mintemp, humidity and wind speed.
    function getForecast ($city): array {
        $country = "US";
        $url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=" . $city . "," . $country . "&units=metric&cnt=1&lang=en&appid=c0c4a4b4047b97ebc5948ac9c48c0559";
        $json = file_get_contents($url);
        // json_decode converts a JSON object into a PHP array.  You will need to use var_dump or print_r to view the structure of the data returned to build your $weather array

        $data = json_decode($json, true);
//        echo '<pre>';
//        var_dump($data);
//        echo'</pre>';

        $weatherData = $data['list'][0];

        $weather = array(
                'maxtemp' => $weatherData['temp']['max'],
                'mintemp' => $weatherData['temp']['min'],
                'description' => $weatherData['weather'][0]['description'],
                'icon' => $weatherData['weather'][0]['icon'],
                'humidity' => $weatherData['humidity'],
                'speed' => $weatherData['speed'],
                'population' => $data['city']['population'],
                'day_temp' => $weatherData['temp']['day'],
                'eve_temp' => $weatherData['temp']['eve'],
                'morn_temp' => $weatherData['temp']['morn'],
                'feels_like' => $weatherData['feels_like']['day'],
                'pressure' => $weatherData['pressure'],
                'gust' => $weatherData['gust']


        );
        return $weather;
    }



    // Check to see if the web FORM was submitted with a city.
    if ((isset($_POST['city']))) {
        $city = $_POST['city'];
        $forecast = getForecast($city);

        // Call your function passing it the city and assign the result to the variable $forecast.
        if ($forecast) {
            echo '
                    <h2>' . $city . ' Weather Forecast</h2>
                    <div class="time">
                        <div>' . date("l g:i a", $currentTime) . '</div>
                        <div>' . date("jS F, Y", $currentTime) . '</div>
                        <div>' . ucwords($forecast['description']) . '</div>
                    </div>
                    <div class="weather-forecast">
                        <img src="https://openweathermap.org/img/w/' . $forecast['icon'] . '.png" class="weather-icon" />
                    High ' . $forecast['maxtemp'] . '°C <span class="min-temperature"> 
                    Low ' . $forecast['mintemp'] . '°C</span>
                </div>
                <div class="time">
                    <div>Humidity: ' . $forecast['humidity'] . ' %</div>
                    <div>Wind: ' . $forecast['speed'] . ' km/h</div>
                </div>';
        }
    } else {
        echo '
                    <form method="POST" action="weatherforecast.php">
                    City: <input type="text" name="city"/><br/><br/>
                    <input type="submit" name="forecast" value="Get Forecast"/>
                    </form>
                ';
    }
    ?>
</div>
</body>
</html>

