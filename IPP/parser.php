<?php

define('INSTR_VAR', '/^(?:(GF|TF|LF)@([a-žA-Ž0-9_\-\$&%\*!?]+))$/');
define('INSTR_SYMB', '/^(?:(GF|TF|LF)@([a-žA-Ž0-9_\-\$&%\*!?]+)|(nil@nil)|(int@[+-]?[0-9]+)|(string@(?:([^\s#\\\\]+)(?!(?9))|(\\\\[0-9]{3})+(?!(?10)))+)|(bool@(true|false))|(string@))$/');
define('INSTR_LABEL', '/^([a-žA-Ž0-9_\-\$&%\*!?]+)$/');
define('INSTR_TYPE', '/^(int|bool|string)$/');

ini_set('display_errors', 'stderr');
$header = false;
$instr_order = 1;

function check_arg(array $splitted, int $count)
{
    if (count($splitted) < $count) {
        return true;
    }

    return false;
}

function write_symbol(string $string, int $arg_count)
{
    if (preg_match('/^int@.*/', $string)) {
        echo "\t\t<arg$arg_count type=\"int\">";
        echo preg_replace('/^int@/', '', $string);
        echo "</arg$arg_count>\n";

        return true;
    } elseif (preg_match('/^bool@.*/', $string)) {
        echo "\t\t<arg$arg_count type=\"bool\">";
        echo preg_replace('/^bool@/', '', $string);
        echo "</arg$arg_count>\n";

        return true;
    } elseif (preg_match('/^nil@nil/', $string)) {
        echo "\t\t<arg$arg_count type=\"nil\">";
        echo 'nil@nil';
        echo "</arg$arg_count>\n";

        return true;
    } elseif (preg_match('/^(LF|TF|GF)@.*/', $string)) {
        echo "\t\t<arg$arg_count type=\"var\">";
        echo preg_replace('/^nil@/', '', $string);
        echo "</arg$arg_count>\n";

        return true;
    } elseif (preg_match('/^string@.*/', $string)) {
        echo "\t\t<arg$arg_count type=\"string\">";
        $helper = preg_replace('/^string@/', '', $string);
        $helper = str_replace(['<', '>', '&', '#'], ['&lt', '&gt', '&amp', '\x053'], $helper);
        echo $helper;
        echo "</arg$arg_count>\n";

        return true;
    }

    return false;
}

if ($argc >= 2) {
    if ($argv[1] == '--help') {
        echo "*** NAPOVEDA ***\n";
        echo "Skript nacte ze standardniho vstupu zdrojovy kod v IPPcode21,\n";
        echo "zkontroluje lexikalni a syntaktickou spravnost kodu\n";
        echo "a vypise na standardni vystup XML reprezentaci programu.\n";
        echo "Use: parser.php [options] <input\n";
        exit(0);
    } else {
        exit(10);
    }
}

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
while ($line = fgets(STDIN)) {
    if (($line == "\n") || (preg_match('~^\s*#~', $line))) { //Ignoruje prazdne riadky + komentare na zaciatku
        continue;
    }
    $line = preg_replace('/\s+/', ' ', $line);
    $line = trim(preg_replace('/#.*$/', '', $line));
    $linetrimmed = trim($line, "\n");
    $splitted = explode(' ', $linetrimmed);

    if ($header == false) {
        if (strtoupper($splitted[0]) == '.IPPCODE21') {
            $header = true;
            echo "<program language=\"IPPcode21\">\n";
        } else {
            exit(21);
        }
    }

    switch (strtoupper($splitted[0])) {
        case 'MOVE':
        case 'INT2CHAR':
        case 'STRLEN':
        case 'TYPE':
            if (check_arg($splitted, 3)) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if ((preg_match(INSTR_VAR, $splitted[1])) && (preg_match(INSTR_SYMB, $splitted[2]))) {
                echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
                if (write_symbol($splitted[2], 2) == false) {
                    exit(23);
                }
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case 'CREATEFRAME':
        case 'PUSHFRAME':
        case 'POPFRAME':
        case 'RETURN':
        case 'BREAK':
            if (check_arg($splitted, 1)) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            echo "\t</instruction>\n";
            ++$instr_order;
            break;

        case 'DEFVAR':
        case 'POPS':
            if (check_arg($splitted, 2)) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if (preg_match(INSTR_VAR, $splitted[1])) {
                echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case 'CALL':
            if (check_arg($splitted, 2)) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if (preg_match(INSTR_LABEL, $splitted[1])) {
                echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case 'PUSHS':
        case 'WRITE':
        case 'EXIT':
        case 'DPRINT':
            if (check_arg($splitted, 2)) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if (preg_match(INSTR_SYMB, $splitted[1])) {
                if (write_symbol($splitted[1], 1) == false) {
                    exit(23);
                }
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case 'READ':
            if (check_arg($splitted, 3)) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if (preg_match(INSTR_TYPE, $splitted[2])) {
                echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
                echo "\t\t<arg2 type=\"type\">$splitted[2]</arg2>\n";
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case 'ADD':
        case 'SUB':
        case 'MUL':
        case 'IDIV':
        case 'LT':
        case 'GT':
        case 'EQ':
        case 'AND':
        case 'OR':
        case 'STRI2INT':
        case 'CONCAT':
        case 'GETCHAR':
        case 'SETCHAR':
            if (check_arg($splitted, 4)) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if ((preg_match(INSTR_VAR, $splitted[1])) && (preg_match(INSTR_SYMB, $splitted[2])) && (preg_match(INSTR_SYMB, $splitted[3]))) {
                echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
                if (write_symbol($splitted[2], 2) == false) {
                    exit(23);
                }
                if (write_symbol($splitted[3], 3) == false) {
                    exit(23);
                }
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case 'NOT':
            if (count($splitted) == 4) {
                echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
                if ((preg_match(INSTR_VAR, $splitted[1])) && (preg_match(INSTR_SYMB, $splitted[2])) && (preg_match(INSTR_SYMB, $splitted[3]))) {
                    echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
                    if (write_symbol($splitted[2], 2) == false) {
                        exit(23);
                    }
                    if (write_symbol($splitted[3], 3) == false) {
                        exit(23);
                    }
                    echo "\t</instruction>\n";
                } else {
                    exit(23);
                }
                ++$instr_order;
                break;
            } elseif (count($splitted) == 3) {
                echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
                if ((preg_match(INSTR_VAR, $splitted[1])) && (preg_match(INSTR_SYMB, $splitted[2]))) {
                    echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
                    if (write_symbol($splitted[2], 2) == false) {
                        exit(23);
                    }
                    echo "\t</instruction>\n";
                } else {
                    exit(23);
                }
                ++$instr_order;
                break;
            } else {
                exit(23);
            }

            // no break
        case 'LABEL':
        case 'JUMP':
            if (check_arg($splitted, 2)) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if (preg_match(INSTR_LABEL, $splitted[1])) {
                echo "\t\t<arg1 type=\"label\">$splitted[1]</arg1>\n";
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case 'JUMPIFEQ':
        case 'JUMPIFNEQ':
            if (check_arg($splitted, 4)) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if ((preg_match(INSTR_LABEL, $splitted[1])) && (preg_match(INSTR_SYMB, $splitted[2])) && (preg_match(INSTR_SYMB, $splitted[3]))) {
                echo "\t\t<arg1 type=\"label\">$splitted[1]</arg1>\n";
                if (write_symbol($splitted[2], 2) == false) {
                    exit(23);
                }
                if (write_symbol($splitted[3], 3) == false) {
                    exit(23);
                }
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case '.IPPCODE21':
            if (check_arg($splitted, 1)) {
                exit(23);
            }
            break;

        default:
            exit(22);
    }
}
echo "</program>\n";
exit(0);
