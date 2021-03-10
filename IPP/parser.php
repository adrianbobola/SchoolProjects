<?php

define('INSTR_VAR', '/(LF|GF|TF)@[a-zA-Z#&*$][a-zA-Z#&*$0-9]*/');
define('INSTR_SYMB', '/(LF|GF|TF|string|bool|int)@[a-zA-Z#&*$\][a-zA-Z#&*$0-9]*/');
define('INSTR_LABEL', '/(end|while)*/');

ini_set('display_errors', 'stderr');
$header = false;
$instr_order = 1;

function check_comments(array $splitted, int $count)
{
    if (count($splitted) < $count) {
        return false;
    }
    if ((count($splitted)) > $count) {
        foreach ($splitted as $key => $value) {
            if (($key > $count - 1) && ((strcmp($value, '') !== 0))) {
                if (strcmp($value[0], '#') == 0) {
                    return true;
                } else {
                    return false;
                }
            }
        }
    }

    return true;
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
            if (count($splitted) < 3) {
                exit(23);
            }
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if ((preg_match(INSTR_VAR, $splitted[1])) && (preg_match(INSTR_SYMB, $splitted[2]))) {
                echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
                echo "\t\t<arg2 type=\"string\">$splitted[2]</arg2>\n";
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
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            echo "\t</instruction>\n";
            ++$instr_order;
            break;

        case 'DEFVAR':
        case 'POPS':
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
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if (preg_match(INSTR_SYMB, $splitted[1])) {
                echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
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
        case 'NOT':
        case 'STRI2INT':
        case 'CONCAT':
        case 'GETCHAR':
        case 'SETCHAR':
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if ((preg_match(INSTR_VAR, $splitted[1])) && (preg_match(INSTR_SYMB, $splitted[2])) && (preg_match(INSTR_SYMB, $splitted[3]))) {
                echo "\t\t<arg1 type=\"var\">$splitted[1]</arg1>\n";
                echo "\t\t<arg2 type=\"string\">$splitted[2]</arg2>\n";
                echo "\t\t<arg3 type=\"string\">$splitted[3]</arg3>\n";
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case 'LABEL':
        case 'JUMP':
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
            echo "\t<instruction order=\"$instr_order\" opcode=\"$splitted[0]\">\n";
            if ((preg_match(INSTR_LABEL, $splitted[1])) && (preg_match(INSTR_SYMB, $splitted[2])) && (preg_match(INSTR_SYMB, $splitted[3]))) {
                echo "\t\t<arg1 type=\"label\">$splitted[1]</arg1>\n";
                echo "\t\t<arg2 type=\"var\">$splitted[2]</arg2>\n";
                echo "\t\t<arg3 type=\"string\">$splitted[3]</arg3>\n";
                echo "\t</instruction>\n";
            } else {
                exit(23);
            }
            ++$instr_order;
            break;

        case '.IPPCODE21':
            if (check_comments($splitted, 1) == false) {
                exit(23);
            }
            break;

        default:
            exit(22);
    }
}
echo "</program>\n";
exit(0);
