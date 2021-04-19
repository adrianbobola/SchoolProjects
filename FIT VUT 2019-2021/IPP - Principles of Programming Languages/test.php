#!/usr/bin/env php
<?php
ini_set('display_errors', 'stderr');

$total_tests = 0;
$passed_tests = 0;
$failed_tests = 0;

function generate_html_start()
{
    echo "<!DOCTYPE html>\n";
    echo "<html lang=\"cz\">\n";
    echo "<head>\n";
    echo "<title>Test.php - IPP</title>\n";
    echo "</head>\n";
    echo "<body>\n";
    echo "<center><h2>IPP 2021 - test.php</h2><br></center>\n";
}

function generate_html_stats()
{
    echo "<h3> --- Test sum: --- <br>\n";
    echo "<p style=\"color:green\">Uspesne:   " . $GLOBALS["passed_tests"] . "</p>\n";
    echo "<p style=\"color:red\">Neuspesne: " . $GLOBALS["failed_tests"] . "</p>\n";
    echo "<p style=\"color:blue\">Celkom   : " . $GLOBALS["total_tests"] . "</p>\n";
    echo "</h3>";
}

function generate_html_end()
{
    echo "</body>\n";
    echo "</html>\n";
}

function create_if_missing_files($directory, $file)
{
    if (!file_exists($directory . $file . '.in')) {
        $new_file = fopen($directory . $file . '.in', 'w');
        fclose($new_file);
    }
    if (!file_exists($directory . $file . '.out')) {
        $new_file = fopen($directory . $file . '.out', 'w');
        fclose($new_file);
    }
    if (!file_exists($directory . $file . '.rc')) {
        $new_file = fopen($directory . $file . '.rc', 'w');
        fwrite($new_file, '0');
        fclose($new_file);
    }
}

function check_files_location($directory, $int_only, $parse_script, $parse_only, $int_script, $jexamxml, $jexamcfg)
{
    if (!file_exists($directory)) {
        fwrite(STDERR, "cesta $directory neexistuje\n");
        exit(41);
    }
    if ($int_only == false) {
        if (!file_exists($parse_script)) {
            fwrite(STDERR, "subor $parse_script neexistuje\n");
            exit(41);
        }
    }
    if ($parse_only == false) {
        if (!file_exists($int_script)) {
            fwrite(STDERR, "subor $int_script neexistuje\n");
            exit(41);
        }
    }
    if (!file_exists($jexamxml)) {
        fwrite(STDERR, "subor $jexamxml neexistuje\n");
        exit(41);
    }
    if (!file_exists($jexamcfg)) {
        fwrite(STDERR, "subor $jexamcfg neexistuje\n");
        exit(41);
    }
}

function chceck_deny_parameters($int_only, $parse_only, $parse_script_bool, $int_script_bool)
{
    if (($int_only == true) and ($parse_only == true)) {
        fwrite(STDERR, "int_only a parse_only sa nesmu kombinovat\n");
        exit(10);
    } elseif (($int_only == true) and ($parse_script_bool == true)) {
        fwrite(STDERR, "int_only a parse_script sa nesmu kombinovat\n");
        exit(10);
    } elseif (($parse_only == true) and ($int_script_bool == true)) {
        fwrite(STDERR, "parse_only a int_script sa nesmu kombinovat\n");
        exit(10);
    }
}

function printing_help()
{
    echo "*** NAPOVEDA skriptu test.php ***\n" .
        "Skript slouzi pro automaticke testovani aplikace parse.php\n" .
        "a aplikace interpret.py\n" .
        "---- Pouzite parametre: ------\n" .
        "--help - zobrazi tuto napovedu\n" .
        "--directory=path - testy bude hladat v zvolenom adresari\n" .
        "--recursive - testy nebude hladat iba v adresari testu, ale rekurzivne aj v jeho podadresaroch\n" .
        "--parse-script=file - subor so skriptom parse.php - ak chyba tak hladam parse.php v aktualnom adresari\n" .
        "--int-script=file - subor so skriptom interpret.py v Python 3.8\n" .
        "--parse-only - testujem iba skript pre analyzu kodu IPPcode21\n" .
        "--int-only - testujem iba skript pre interpret kodu IPPcode21\n" .
        "--jexamxml=file - subor s JAR balickom s nastrojom A7Soft JExamXML\n" .
        "--jexamcfg=file - subor s konfiguraciou nastroja A7Soft JExamXML\n";
}

if ($argc == 1) { //no parameters
    fwrite(STDERR, "Neboli zadane ziadne parametre\n");
    exit(10);
} elseif ($argc > 9) { //too much parameters
    fwrite(STDERR, "Prilis vela zadanych parametrov\n");
    exit(10);
}

$directory = getcwd();
$recursive = false;
$parse_script = getcwd() . "/parse.php";;
$parse_script_bool = false;
$int_script = getcwd() . "/interpret.py";;
$int_script_bool = false;
$parse_only = false;
$int_only = false;
$jexamxml = "/pub/courses/ipp/jexamxml/jexamxml.jar";
$jexamcfg = "/pub/courses/ipp/jexamxml/options";

$help_with_another_param = false;
$print_help = false;
for ($i = 1; $i < $argc; $i++) {
    if ($argv[$i] == '--help') {
        $print_help = true;
    } else {
        $help_with_another_param = true;
    }

}
if (($print_help == true) and ($help_with_another_param == false)) {
    printing_help();
    exit(0);
} elseif (($print_help == true) and ($help_with_another_param == true)) {
    fwrite(STDERR, "Parameter help nesmie obsahovat ine parametre\n");
    exit(10);
}

for ($i = 1; $i < $argc; $i++) {
    $argv_explode = explode("=", $argv[$i]);
    if ($argv_explode[0] == "--directory") {
        $argv_explode = explode("=", $argv[$i]);
        if (!array_key_exists(1, $argv_explode)) {
            fwrite(STDERR, "nezadana cesta k suboru directory\n");
            exit(10);
        }
        $directory = $argv_explode[1];
    } elseif ($argv_explode[0] == "--recursive") {
        $recursive = true;
    } elseif ($argv_explode[0] == "--parse-script") {
        if (!array_key_exists(1, $argv_explode)) {
            fwrite(STDERR, "nezadana cesta k suboru parse-script\n");
            exit(10);
        }
        $parse_script = $argv_explode[1];
        $parse_script_bool = true;
    } elseif ($argv_explode[0] == "--int-script") {
        if (!array_key_exists(1, $argv_explode)) {
            fwrite(STDERR, "nezadana cesta k suboru int-script\n");
            exit(10);
        }
        $int_script = $argv_explode[1];
        $int_script_bool = true;
    } elseif ($argv_explode[0] == "--parse-only") {
        $parse_only = true;
    } elseif ($argv_explode[0] == "--int-only") {
        $int_only = true;
    } elseif ($argv_explode[0] == "--jexamxml") {
        if (!array_key_exists(1, $argv_explode)) {
            fwrite(STDERR, "nezadana cesta k suboru jexamxml\n");
            exit(10);
        }
        $jexamxml = $argv_explode[1];
    } elseif ($argv_explode[0] == "--jexamcfg") {
        if (!array_key_exists(1, $argv_explode)) {
            fwrite(STDERR, "nezadana cesta k suboru jexamcfg\n");
            exit(10);
        }
        $jexamcfg = $argv_explode[1];
    } else {
        fwrite(STDERR, "Invalid argument\n");
        exit(10);
    }
}

chceck_deny_parameters($int_only, $parse_only, $parse_script_bool, $int_script_bool);
check_files_location($directory, $int_only, $parse_script, $parse_only, $int_script, $jexamxml, $jexamcfg);
generate_html_start();

$result_stats = array();
$files = explode("\n", shell_exec('ls ' . $directory . ' 2>/dev/null | grep .src'));
foreach ($files as $file) {
    $file = str_replace('.src', '', $file); //odstran priponu .src suboru
    if ($file == "") {
        continue;
    } elseif ($file == ".") {
        continue;
    } elseif ($file == "..") {
        continue;
    }
    create_if_missing_files($directory, $file);

    // Parse.php
    if ($int_only == false) {
        $output = NULL;
        $result = array();
        exec('cat ' . $directory . $file . '.src | php7.4 ' . $parse_script . '> tmp_output_parser', $output, $parser_return_code);
        $ref_return_code_file = fopen($directory . '/' . $file . '.rc', 'r');
        $ref_return_code = fgets($ref_return_code_file);
        if ($ref_return_code == $parser_return_code) { //RC je zhodny s testovym RC
            if ($parser_return_code == 0) { //RC je 0 -> pouzijem JExamXml
                exec('java -jar ' . $jexamxml . ' tmp_output_parser ' . $directory . "/" . $file . ".out tmp_output_parser " . $jexamcfg . "> tmp_xml_test");
                $xml_test = fopen('tmp_xml_test', 'r');
                while (($line_test = fgets($xml_test)) != false) {
                    if ($line_test == "Two files are identical\n") {


                        if ($parse_only == false) { //spusti interpret
                            exec('python3 ' . $int_script . ' --source=tmp_output_parser < ' . $directory . '/' . $file . '.in > tmp_output_interpret', $output, $interpret_return_code);
                            if ($ref_return_code == $interpret_return_code) { //RC je zhodny s testovym RC
                                if ($interpret_return_code == 0) { //RC je 0 -> pouzijem diff
                                    exec('diff tmp_output_interpret ' . $directory . "/" . $file . '.out', $output, $diff_return_code);
                                    if ($diff_return_code == 0){ //su zhodne
                                        print("******OK******");
                                        array_push($result, $GLOBALS["total_tests"], $file, $directory, $interpret_return_code, $ref_return_code, "OK");
                                    }
                                    else{ //diff hlasi nezhodu
                                        print("******NEOK******");
                                        array_push($result, $GLOBALS["total_tests"], $file, $directory, $interpret_return_code, $ref_return_code, "FAILED-INTERPRET");
                                    }
                                }
                                else { //RC nie je 0
                                    print("******OK******");
                                    array_push($result, $GLOBALS["total_tests"], $file, $directory, $interpret_return_code, $ref_return_code, "OK");
                                }
                            } else { //RC nie je zhodny s RC testu
                                array_push($result, $GLOBALS["total_tests"], $file, $directory, $interpret_return_code, $ref_return_code, "FAILED-INTERPRET");
                            }



                        } else { //nespustam interpret
                            array_push($result, $GLOBALS["total_tests"], $file, $directory, $parser_return_code, $ref_return_code, "OK");
                        }

                        /*
                        echo "Test cislo " . $GLOBALS["total_tests"] . ": <b>$file</b> v priecinku: <b>$directory</b>:\n";
                        echo "Navratovy kod:<b>" . $parser_return_code . "</b> | Spravny navratovy kod: <b>$ref_return_code</b><p style=\"color:green\"><b>OK</b></p>\n";
                        echo "----------------------------------------------------------------------------------------------------------------------------<br>\n";
                        $GLOBALS["passed_tests"]++;
                        */
                    }
                }
                fclose($xml_test);
            } else { //RC nie je 0
                if ($parse_only == false) { //spusti interpret
                    exec('python3 ' . $int_script . ' --source=tmp_output_parser < ' . $directory . '/' . $file . '.in > tmp_output_interpret', $output, $interpret_return_code);
                    if ($ref_return_code == $interpret_return_code) { //RC je zhodny s testovym RC
                        if ($interpret_return_code == 0) { //RC je 0 -> pouzijem diff
                            exec('diff tmp_output_interpret ' . $directory . "/" . $file . '.out', $output, $diff_return_code);
                            if ($diff_return_code == 0){ //su zhodne
                                print("******OK******");
                                array_push($result, $GLOBALS["total_tests"], $file, $directory, $interpret_return_code, $ref_return_code, "OK");
                            }
                            else{ //diff hlasi nezhodu
                                print("******NEOK******");
                                array_push($result, $GLOBALS["total_tests"], $file, $directory, $interpret_return_code, $ref_return_code, "FAILED-INTERPRET");
                            }
                        }
                        else { //RC nie je 0
                            array_push($result, $GLOBALS["total_tests"], $file, $directory, $interpret_return_code, $ref_return_code, "OK");
                        }
                    } else { //RC nie je zhodny s RC testu
                        array_push($result, $GLOBALS["total_tests"], $file, $directory, $interpret_return_code, $ref_return_code, "FAILED-INTERPRET");
                    }
                } else { //nespustam interpret
                    array_push($result, $GLOBALS["total_tests"], $file, $directory, $parser_return_code, $ref_return_code, "OK");
                }
            }
        } else { //RC nie je zhodny s testovym RC
            echo "Test cislo " . $GLOBALS["total_tests"] . ": <b>$file</b> v priecinku: <b>$directory</b>:\n";
            echo "Navratovy kod:<b>" . $parser_return_code . "</b> | Spravny navratovy kod: <b>$ref_return_code</b><p style=\"color:red\"><b>FAILED</b></p>\n";
            echo "----------------------------------------------------------------------------------------------------------------------------<br>\n";
            $GLOBALS["failed_tests"]++;
            array_push($result, $GLOBALS["total_tests"], $file, $directory, $parser_return_code, $ref_return_code, "FAILED-PARSE");
        }
        exec('rm -f tmp_xml_test');
        fclose($ref_return_code_file);
        $GLOBALS["total_tests"]++;
        array_push($result_stats, $result);
    }

    // Interpret
    if ($int_only == true) { //TODO: BEZ PARSRU
        exit(9999);
    }
}
generate_html_stats();


echo "<h3> ---- Parametre test.php: ----</h3>\n";
echo "--directory = $directory <br>\n";
echo "--parse-script = $parse_script <br>\n";
echo "--int-script = $int_script <br>\n";
echo "--jexamxml = $jexamxml <br>\n";
echo "--jexamcfg = $jexamcfg <br>\n";
echo "<h3> ---- Aktivovane parametre: ----</h3>\n";
if ($recursive == true) {
    echo "--recursive<br>\n";
}
if ($parse_only == true) {
    echo "--parse_only<br>\n";
}
if ($int_only == true) {
    echo "--int_only<br>\n";
}
generate_html_end();
