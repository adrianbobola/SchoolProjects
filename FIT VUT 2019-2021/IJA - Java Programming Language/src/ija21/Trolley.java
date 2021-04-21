/*
  Class Trolley represent a trolley in the map.
  @author Ladislav Dokoupil (xdokou14)
  @author Adrián Bobola (xbobol00)
 */

package ija21;

import java.util.Map;

public class Trolley extends Storeable {
    private final int id;
    private final int capacity;

    public Map.Entry<String, Integer> task;

    /**
     * Save trolley data into local structures task
     * @param id_in trolley ID
     * @param cord  trolley coordinates (contains X and Y)
     */
    public Trolley(int id_in, Coordinates cord) {
        super(cord.x, cord.y);
        this.id = id_in;
        this.capacity = 5;
    }

    /**
     * get trolley ID
     * @return trolley ID
     */
    public int getId() {
        return id;
    }

    /**
     * get amount of items in trolley
     * @return amount of items
     */
    public int getItemInCount() {
        return this.getStored().size();
    }

    /**
     * get trolley capacity
     * @return trolley capacity
     */
    public int getCapacity() {
        return this.capacity;
    }
}
