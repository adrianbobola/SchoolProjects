package sample;

/*import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;*/

import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class Main {


    /*Pane root; extends Application

    @Override
    public void start(Stage primaryStage){*/


        /*<taskdef resource="com/sun/javafx/tools/ant/antlib.xml"
        uri="javafx:com.sun.javafx.tools.ant" classpath=".:C:\Program Files\Java\jdk1.7.0_09\lib\ant-javafx.jar"/>*/
        /*Button btn = new Button();
        btn.setText("Say 'Hello World'");*/

        /*btn.setOnAction(actionEvent -> {
            btn.setLayoutX(btn.getLayoutX() + 10);
            btn.setLayoutY(btn.getLayoutY() + 10);
        })

        //root = new Pane();
        /*root.getChildren().add(btn);
        btn.setLayoutX(10);
        btn.setLayoutY(10);*/

        /*Scene scene = new Scene(root, 300, 250);

        primaryStage.setTitle("Hello World!");
        primaryStage.setScene(scene);
        primaryStage.show();*/
    //}

    public static void changeTrolleyPosition(Trolley trolley, int requireItemNumber, String[][] map){
        //Changing trolley X-sur
        if (trolley.x < trolley.newPosition[0][requireItemNumber][0]) {
            trolley.moveX(1);
        } else if (trolley.x > trolley.newPosition[0][requireItemNumber][0]) {
            trolley.moveX(-1);
        }

        //Changing trolley y-sur
        if (trolley.y < trolley.newPosition[0][requireItemNumber][1]) {
            trolley.moveY(1);
        } else if (trolley.y > trolley.newPosition[0][requireItemNumber][1]) {
            trolley.moveY(-1);
        }
        map[trolley.y][trolley.x] = "T";

    }

    public static void printMap(String[][] map){
        for (int row = 0; row < map.length; row++) {
            for (int col = 0; col < map[row].length; col++) {
                System.out.print(map[row][col]);
            }
            System.out.println("");
        }
    }

    public static void main(String[] args) {
        //launch(args);
        JsonParser jsonParser = null;
        try {
            jsonParser = new JsonParser("sample.json");
        } catch (Exception e) {
            System.err.println("chyba parser: sample.json");
            System.exit(1);
        }
        final int maxX = jsonParser.getMaxX();
        final int maxY = jsonParser.getMaxY();


        RequirementsParser reqParser = null;
        try {
            reqParser = new RequirementsParser("requirements.json");
        } catch (Exception e) {
            System.err.println("chyba parser: requirements.json");
            System.exit(2);
        }

        jsonParser.getAllGoods().forEach((cordinates, tmp) -> {
            System.out.println("Stored-Obj: " + cordinates.x + " : " + cordinates.y + " " + tmp);
        });
        System.out.println("----------------------------------------------------------");
        reqParser.requirements.forEach((name, count) -> {
            System.out.println("REQUIRE-name: " + name + ", require amount: " + count);
        });
        System.out.println("\n**************************************************************************");
        System.out.println("*************************  ITEMS *****************************************");
        System.out.println("**************************************************************************\n\n");

        //initalize pathifinding sturcure
        FindPath findPath = new FindPath(maxX, maxY);
        //update every time shelfs are changed
        findPath.updatePaths(jsonParser.getAllGoods());


        JsonParser finalJsonParser = jsonParser;
        reqParser.requirements.forEach((name, count) -> {
            Cordinates myPositionCord = new Cordinates(finalJsonParser.getTrolleys().get(0).x, finalJsonParser.getTrolleys().get(0).y);

            TreeMap<Double, Cordinates> sortedByDistances = new TreeMap<>();
            int RequiredItemsAmount = count;
            Map<Cordinates, Shelf> found = finalJsonParser.findGoods(name);

            if (found.size() < 1) {
                System.out.println("!!!!!!! ERROR: POZADOVANA POLOZKA: " + name + " NENI SKLADEM !!!!!!!!!");
            }

            for (Map.Entry<Cordinates, Shelf> entry : found.entrySet()) {
                int x = entry.getKey().x;//cordinate
                int y = entry.getKey().y;
                //entry.getValue();//shelf
                int countItemsInShelf = entry.getValue().stored.get(name);
                double distance = entry.getKey().getDistance(myPositionCord);
                sortedByDistances.put(distance, entry.getKey());

                System.out.println("name: " + name);
                System.out.println("x: " + x);
                System.out.println("y: " + y);
                System.out.println("shelf count: " + countItemsInShelf);
                System.out.println("distance: " + distance);

                System.out.println("---------------------------");
                System.out.print("POCET POLOZIEK NA SKLADE: ");
                if (found.size() == 1) { //polozka je iba v 1 Shelfe
                    if (RequiredItemsAmount <= countItemsInShelf) {
                        System.out.println("OK");
                        //TODO: delete_item + poslat vozik k regalu + mnozstvi polozek ve voziku++
                    } else {    //ERROR - chcem viac ks ako mame na sklade
                        System.out.println("!!!!!!! ERROR: POZADOVANE MNOZSTVI NENI SKLADEM !!!!!!!!!");
                    }
                } else {    //polozka je vo viacerych shelf-och
                    System.out.println("Polozka je vo viacerich shelf-och TODO:NENI implementovano");
                    //TODO: vybrat najblizsi regal + zistit ci postacuje mnozstvo na nom alebo pridat aj dalsi regal
                }
                System.out.println("---------------------------");
            }


            if (sortedByDistances.size() != 0) {
                Cordinates lowestDisanceCord = sortedByDistances.firstEntry().getValue(); //min distance Cordinates value
                System.out.println("(CHECKING): Vybrana kratsia vzdialenost ma suradnice: x:" + lowestDisanceCord.x + " y:" + lowestDisanceCord.y);
                PathNode vysl2 = findPath.aStar(myPositionCord, lowestDisanceCord);


                int changingSurCounter = 0;
                while (vysl2 != null) {
                    //System.out.print(vysl2 + "->");
                    Trolley trolley = finalJsonParser.getTrolleys().get(0);
                    trolley.addNewPosition(0, changingSurCounter, vysl2.self.x, vysl2.self.y);
                    //System.out.println("Vozik ma suradnice: x:" + myPositionCord.x + " y:" +myPositionCord.y);
                    System.out.println("PRIDAVAM TROLEY_MOVE : x:" + vysl2.self.x + " y:" + vysl2.self.y);
                    //System.out.println("--------------------------------------------------------");

                    vysl2 = vysl2.parent;
                    changingSurCounter++;
                }
                //System.out.println("PATH_END");
                //System.out.println("ASTAR OUTPUT: " + vysl2);
            }
            System.out.println();
            System.out.println("************************* NEXT ITEM *****************************************");
            System.out.println();
        });

        Boolean running = true;
        while (running) {
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            //Create empty map
            String[][] map = new String[maxX][maxY];
            for (String[] row : map) {
                Arrays.fill(row, " ");
            }

            //put all shelf into map
            jsonParser.getAllGoods().forEach((cordinates, tmp) -> {
                map[cordinates.y][cordinates.x] = "X";
            });

            //put all trolley into map
            map[finalJsonParser.getTrolleys().get(0).y][finalJsonParser.getTrolleys().get(0).x] = "T";

            //print map
            printMap(map);

            System.out.println("--------- NEXT MAP UPDATE -----------------");
            Trolley trolley = finalJsonParser.getTrolleys().get(0);
            for (int requireItemNumber = trolley.newPosition[0].length - 1; requireItemNumber >= 0; requireItemNumber--) {
                if (trolley.newPosition[0][requireItemNumber][0] != null) {
                    //mazanie cesty vozika
                    //map[trolley.y][trolley.x] = " ";

                    //System.out.print("new X:" + trolley.newPosition[0][requireItemNumber][0]);
                    //System.out.print(", Y:" + trolley.newPosition[0][requireItemNumber][1]);
                    changeTrolleyPosition(trolley, requireItemNumber, map);

                    //System.out.println("");
                    System.out.println("Vozik ma NOVE suradnice: x:" + trolley.x + " y:" + trolley.y);
                    //System.out.println("---------------------------------------------------------");
                    printMap(map);
                    System.out.println("--------- NEXT MAP UPDATE -----------------");
                }
            }
            running = false;
        }
    }
}
