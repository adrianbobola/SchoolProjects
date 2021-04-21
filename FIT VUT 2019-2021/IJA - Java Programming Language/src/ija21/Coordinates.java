/*
  Class Cordinates represent x and y coordinates of object
  @author Ladislav Dokoupil (xdokou14)
  @author Adrián Bobola (xbobol00)
 */

package ija21;

import java.util.Objects;

public class Coordinates {
    int x, y;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Coordinates that = (Coordinates) o;
        return x == that.x && y == that.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    /**
     * cordinate position
     * @param x position on horizontal axis
     * @param y position on vertical axis
     */
    public Coordinates(int x, int y){
        this.x = x;
        this.y = y;
    }
    /**
     * get straight line distance between two cordinates
     * @param cord 2.nd cordinate
     * @return distance of cordinates
     */
    public double getDistance(Coordinates cord){
        return Math.sqrt(Math.pow(this.x - cord.x,2) + Math.pow(this.y - cord.y,2));
    }
}
