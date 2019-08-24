<!DOCTYPE html>
<html>

<head>
	<Title>Palette Switch</Title>
</head>


<body>
	<p><a href="./index.html">Home</a></p>

	<ul>
	<?php
		$results_dir = '../uploads/';
		$dir = opendir($results_dir);
		$filename_list = array();

		while (false !== ($file = readdir($dir)))
		{
			if ($file == "." || $file == "..")
				continue;
			array_push($filename_list, $file);
		}
		closedir($dir);
		sort($filename_list);

		foreach ($filename_list as $each_dir)
		{
			echo "<li><a href=\"$results_dir$each_dir/list.php\">$each_dir</a></li><br />";
		}
	?>
		<!--<li><a href="./.html"></a></li>-->
	</ul>

</body>

</html>





































