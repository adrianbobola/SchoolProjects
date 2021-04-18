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

function test_files($directory)
{
    // Nacteni jednotlivych souboru s koncovkou .src TODO
    $files = explode("\n", shell_exec('ls ' . $directory . ' 2>/dev/null | grep .src'));
    foreach ($files as $file) {
        if ($file == "") {
            break;
        } elseif ($file == ".") {
            continue;
        } elseif ($file == "..") {
            continue;
        }

        /*
                // Vytvoreni souboru a naplneni predepsanymi hodnotami, pokud jiz neexistuji TODO
                if (!file_exists($directory . rtrim($file, ".src") . '.in')) {
                    $file_create = fopen($directory . rtrim($file, ".src") . '.in', 'w');
                    fclose($file_create);
                }
                if (!file_exists($directory . rtrim($file, ".src") . '.out')) {
                    $file_create = fopen($directory . rtrim($file, ".src") . '.out', 'w');
                    fclose($file_create);
                }
                if (!file_exists($directory . rtrim($file, ".src") . '.rc')) {
                    $file_create = fopen($directory . rtrim($file, ".src") . '.rc', 'w');
                    fwrite($file_create, '0');
                    fclose($file_create);
                }
        */

        $tmpFile = tmpfile();
        $output = NULL;
        // Poslani zdrojoveho kodu obsazeneho v .src souboru do parseru TODO: parse.php nemusi byt v tejto slozke
        exec('cat ' . $directory . '/' . $file . '| php7.4 ' . 'parse.php' . ' 2>/dev/null', $output, $returnHelper);

        $file = str_replace('.src', '', $file);

        if (!file_exists($directory . '/' . $file . '.rc')) {
            $ref_return_code = 0;
        } else {
            $rcFile = fopen($directory . '/' . $file . '.rc', 'r');
            $ref_return_code = fgets($rcFile);
        }
        if ($ref_return_code == $returnHelper) {
            echo "Test cislo " . $GLOBALS["total_tests"] . ": <b>$file</b> v priecinku: <b>$directory</b>:\n";
            echo "Navratovy kod:<b>" . $returnHelper . "</b> | Spravny navratovy kod: <b>$ref_return_code</b><p style=\"color:green\"><b>OK</b></p>\n";
            echo "----------------------------------------------------------------------------------------------------------------------------<br>\n";
            $GLOBALS["passed_tests"]++;
        } else {
            echo "Test cislo " . $GLOBALS["total_tests"] . ": <b>$file</b> v priecinku: <b>$directory</b>:\n";
            echo "Navratovy kod:<b>" . $returnHelper . "</b> | Spravny navratovy kod: <b>$ref_return_code</b><p style=\"color:red\"><b>FAILED</b></p>\n";
            echo "----------------------------------------------------------------------------------------------------------------------------<br>\n";
            $GLOBALS["failed_tests"]++;
        }
        fclose($rcFile);
        $GLOBALS["total_tests"]++;
    }

}

function generate_html_end()
{
    echo "</body>\n";
    echo "</html>\n";
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
    echo "*** NAPOVEDA skriptu test.php ***\n";
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

generate_html_start();
test_files($directory);
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

