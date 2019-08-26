<!DOCTYPE html>
<html>

<head>
	<Title>TW Image Converter</Title>
</head>

<body>
	<?php
/* TODO
connect python
set original images front and show palette


done
check special character in prefix field
add milliseconds to directoryname
connect click to results
	> have to make web page to show results images
*/


		main();

		function main()
		{
			//showArray($_POST);			
			checkError();

			$base_dir = '../uploads/';
			$dir_name = getCurrentTime();
			$dir_path = $base_dir.$dir_name."/";

			mkdir($dir_path, 0755);
			makeImageListingPHPFile($dir_path, $_POST['prefix']);
			saveImagesToNewDirectory($dir_path, $_POST['prefix']);

			runPythonImageConverter($dir_path, $_POST);
		}

		function checkError()
		{
			checkPostMaxSizeError();
			checkFileUploadError();
			checkImgType();
			checkPostValues();
			//checkSQLInjection();
		}

		function getCurrentTime()
		{
			$up_to_sec = date('YmdHis');
			$t = microtime(TRUE);
			$down_from_sec = str_pad(floor(($t - floor($t))*1000), 3, '0', STR_PAD_LEFT);
			return $up_to_sec.$down_from_sec;
		}

		function makeImageListingPHPFile($_dir_path, $_prefix)
		{
			$fp = fopen($_dir_path."list.php", 'w');

			if (!$fp)
			{
				echo "Problem: Cannot make listing php file.";
				exit;
			}

			$php_string = "<!DOCTYPE html>
<html>
<head>
	<Title>List</Title>
</head>


<body>
	<p><a href=\"../../index.html\">Home</a></p>
	<h2>This is temporary directory. Download before leave this page.</h2>
	<?php
		\$images_dir = '.';
		\$dir = opendir(\$images_dir);
		\$filename_list = array();

		//while (false !== (\$file = readdir(\$dir)))
		for (\$i = 0; \$i < 100; \$i++)
		{
			if (\$file = readdir(\$dir))
				array_push(\$filename_list, \$file);
			else
				break;
		}
		closedir(\$dir);

		sort(\$filename_list);

		echo '<figure> <img src=\"./original.png\" width=\"320\", height=\"240\" /> <br /> <figcaption>original.png</figcaption> </figure>';
		for (\$x = 0; \$x < count(\$filename_list); \$x++)
		{
/*
			\$file_ext = preg_split(\"/\./\", \$filename_list[\$x]);
			if (\$file_ext[sizeof(\$file_ext)-1] != \"png\" || preg_match('/".$_prefix."_original_\d+\.png/', \$filename_list[\$x]))
				continue;
			else
				echo '<figure> <img src=\"'.\$filename_list[\$x].'\" width=\"320\", height=\"240\" /> <br /> <figcaption>'.\$filename_list[\$x].'</figcaption> </figure>';
*/

			if (preg_match('/".$_prefix."_\d+\.png/', \$filename_list[\$x]))
				echo '<figure> <img src=\"'.\$filename_list[\$x].'\" width=\"320\", height=\"240\" /> <br /> <figcaption>'.\$filename_list[\$x].'</figcaption> </figure>';
		
		}
	?>

</body>
</html>
";

			fwrite($fp, $php_string);
			fclose($fp);
		}

		function saveImagesToNewDirectory($_dir_path, $_prefix)
		{
			for ($i=0; $i<sizeof($_FILES['images']['name']); $i++)
			{
				$new_file_name = $_dir_path.$_prefix.'_original_'.str_pad($i, 2, '0', STR_PAD_LEFT).'.png';
				//$uploaded_file = $_dir_path.$_FILES['images']['name'][$i];
	
				if (is_uploaded_file($_FILES['images']['tmp_name'][$i]))
				{
					if (!move_uploaded_file($_FILES['images']['tmp_name'][$i], $new_file_name))
					{
						echo 'Problem: Could not move file to destination directory.';
						exit;
					}
				}
				else
				{
					echo 'Problem: Possible file upload attack. Filename: ';
					echo $_FILES['images']['name'][$i];
					exit;
				}
	
			}
		}

		function runPythonImageConverter($_dir_path, $_my_post)
		{
#			echo "<h1>Converting is on going.<br />Please wait \"Done\" message.</h1>";

			$arguments = '';
			$arguments = $arguments.$_dir_path;
			$arguments = $arguments." ".$_my_post['prefix'];
			foreach ($_my_post['colors'] as $idx => $each_color)
				$arguments = $arguments." '".$each_color."'";

			$run = exec("python3 ../python_scripts/tw_cover_image_with_palette.py $arguments");

			echo "<h1>Done!!!</h1>";
			echo "<p>$run</p>";
			echo "<h2><a href=\"".$_dir_path."list.php\">Click here to see the result</a></h2>";
		}

		function checkPostMaxSizeError()
		{
			if (empty($_POST))
			{
				echo 'Problem: Total size of files might exceed post_max_size.';
				exit;
			}
		}

		function checkFileUploadError()
		{
			foreach($_FILES['images']['error'] as $each_error)
			{
				if ($each_error > 0)
				{
					echo 'Problem:';
					switch ($each_error)
					{
						case 1:
							echo 'File exceeded upload_max_filesize.';
							break;
						case 2:
							echo 'File exceeded max_file_size.';
							break;
						case 3:
							echo 'File only partially uploaded.';
							break;
						case 4:
							echo 'No file uploaded.';
							break;
						case 6:
							echo 'Cannot upload file: No temp directory specified.';
							break;
						case 7:
							echo 'Upload failed: Cannot write to disk.';
							break;
						case 8:
							echo 'A PHP extension blocked the file upload.';
							break;
					}
					exit;
				}
			}

		}

		function checkImgType()
		{
			foreach ($_FILES['images']['type'] as $each_type)
			{
				if ($each_type != 'image/png')
				{
					echo 'Problem: file is not a PNG image.';
					exit;
				}
			}
		}

		function checkPostValues()
		{
			// prefix check
			if (!array_key_exists('prefix', $_POST))
			{
				echo 'Problem: Do not change page source.';
				exit;
			}
			else if (!(gettype($_POST['prefix']) == 'string'))
			{
				echo 'Problem: Do not change page source.';
				exit;
			}
			else
			{
				preg_match("/[a-zA-Z0-9_]+/", $_POST['prefix'], $matched_prefix);
				if ($matched_prefix[0] != $_POST['prefix'])
				{
					echo 'Problem: Only use alphabet, number and underscore.';
					exit;
				}
			}
			$_POST['prefix'] = substr($_POST['prefix'], 0, 32);

			// colors check
			if (!array_key_exists('colors', $_POST))
			{
				echo 'Problem: Do not change page source.';
				exit;
			}
			else
			{
				for ($i = 0; $i < sizeof($_POST['colors']); $i++)
				{
					$each_color = $_POST['colors'][$i];

					if (!(gettype($each_color) == 'string'))
					{
						echo 'Problem: Do not change page source.';
						exit;
					}
					else if (!(preg_match("/^#[0-9a-fA-F]{6}/", $each_color, $each_matched_pattern) === 1))
					{
						echo 'Problem: Do not change page source.1';
						exit;
					}
					else
						$_POST['colors'][$i] = $each_matched_pattern[0];
				}
			}

		}

		function checkSQLInjection()
		{
			if (preg_match("/script/i", $_POST['prefix']) === 1)
			{
				echo 'Do not include "script" in prefix';
				exit;
			}
		}

		function showArray($array)
		{
			foreach ($array as $key => $value)
			{
				echo "$key<br />";
				if (is_array($value))
					showArray($value);
				else
					echo " => $value<br />";
			}
		}
	?>
</body>

</html>




















