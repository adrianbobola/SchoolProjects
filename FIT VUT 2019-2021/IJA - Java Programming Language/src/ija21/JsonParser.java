/*
  Class JsonParser
  @author Ladislav Dokoupil (xdokou14)
  @author Adrián Bobola (xbobol00)
 */
package ija21;


import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import java.util.stream.Collectors;
import java.io.FileReader;
import java.util.*;

public class JsonParser {




    private final Map<Coordinates, Shelf> storedObjects = new Hashtable<>();
    private final List<Trolley> trolleyObjects = new ArrayList<>();
    private final List<Coordinates> stagingObjects = new ArrayList<>();
    private final int maxX;
    private final int maxY;


    /**
     * Parses JSON file into local structures storedObjects, trolleyObjects and stagingObjects
     * @param filename file path
     * @throws Exception no such file found or bad JSON structure
     */
    public JsonParser(String filename) throws Exception {
        //praparing json file
        JSONObject obj = (JSONObject) new JSONParser().parse(new FileReader(filename));
        JSONArray content = (JSONArray) obj.getOrDefault("content", new JSONArray());
        JSONArray trolley = (JSONArray) obj.getOrDefault("trolley", new JSONArray());
        JSONArray staging = (JSONArray) obj.getOrDefault("staging", new JSONArray());

        maxX = ((Long) obj.get("maxX")).intValue();
        maxY = ((Long) obj.get("maxY")).intValue();

        // iterating gooods
        Iterator iterator = content.iterator();
        while (iterator.hasNext()) {
            Map entry = ((Map) iterator.next());
            int x = ((Long) entry.get("x")).intValue();
            int y = ((Long) entry.get("y")).intValue();
            Coordinates co = new Coordinates(x, y);
            String name = entry.get("name").toString();
            int amount = ((Long) entry.get("amount")).intValue();
            Shelf tmp = storedObjects.getOrDefault(co, new Shelf(co));
            tmp.add_item(name, amount);
            storedObjects.put(co, tmp);
        }

        //iterating trolleys
        iterator = trolley.iterator();
        while (iterator.hasNext()) {
            Map entry = ((Map) iterator.next());
            int id = ((Long) entry.get("id")).intValue();
            int x = ((Long) entry.get("x")).intValue();
            int y = ((Long) entry.get("y")).intValue();
            Coordinates co = new Coordinates(x, y);
            Trolley ntrolley = new Trolley(id,co);
            trolleyObjects.add(ntrolley);
        }

        //iterating staging arreas
        iterator = staging.iterator();
        while (iterator.hasNext()) {
            Map entry = ((Map) iterator.next());
            int x = ((Long) entry.get("x")).intValue();
            int y = ((Long) entry.get("y")).intValue();
            Coordinates co = new Coordinates(x, y);
            stagingObjects.add(co);
        }
    }

    /**
     * searches all shelfs for item with given name
     * @param name goods name to be searched
     * @return shelfs including item with given name
     */
    Map<Coordinates, Shelf> findGoods(String name){
        Map<Coordinates, Shelf> result;
        result = storedObjects.entrySet()
                .stream()
                .filter(map-> map.getValue().getStored().containsKey(name))
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
        return result;
    }

    /**
     * get stored shelfs
     * @return all existing shelfs
     */
    Map<Coordinates, Shelf> getAllShelfs(){
        return storedObjects;
    }
    /**
     * get stored trolleys
     * @return all existing trolleys
     */
    List<Trolley> getTrolleys(){
        return trolleyObjects;
    }
    /**
     * get stored staging area cordinates
     * @return all existing staging areas
     */
    List<Coordinates> getStages() {
        return stagingObjects;
    }

    /**
     * accessible JSON structures are limited to 0-maxX on x axis
     * @return map limit in horizontal axis
     */
    public int getMaxX() {
        return maxX;
    }

    /**
     * accessible JSON structures are limited to 0-maxY on y axis
     * @return map limit in vertical axis
     */
    public int getMaxY() {
        return maxY;
    }
}
