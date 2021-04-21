/*
  Class FindPatch find the shortest patch from trolley to shelf
  @author Ladislav Dokoupil (xdokou14)
  @author Adrián Bobola (xbobol00)
 */

package ija21;

import java.util.Hashtable;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Queue;

public class FindPath {


    private Map<Coordinates, PathNode> paths = new Hashtable<>();
    private int maxX, maxY;

    /**
     * initalize map limits
     * @param maxX horizontal limit 0-maxX
     * @param maxY vertical limit 0-maxY
     */
     public FindPath(int maxX, int maxY){
         this.maxX = maxX;
         this.maxY = maxY;
     }


    /**
     * shelfs (additions) need to be updated after every user interaction
     * @param shelfs list of all existing shelfs
     */
    public void updatePaths( Map<Coordinates, Shelf> shelfs){

        //make new paths (complement of shelfs with respect to 0-maxX and 0-maxY)
        paths.clear();
        for (int x = 0; x <= maxX; x++) {
            for (int y = 0; y <= maxY; y++) {
                Coordinates position = new Coordinates(x,y);
                //is shelf
                if(shelfs.containsKey(position))
                    continue;
                paths.put(position,new PathNode(position));
            }
        }

        //add neighbours for each path
        for(Map.Entry<Coordinates, PathNode> entry : paths.entrySet()){
            int x = entry.getKey().x;
            int y = entry.getKey().y;

            //check 3x3 space around Node 
            for(int x1=x-1;x1<=x+1;x1++){
                for(int y1=y-1;y1<=y+1;y1++){
                    Coordinates seek = new Coordinates(x1,y1);
                    //out of bounds
                    if (x1 < 0 || x1 > maxX || y1 < 0 || y1 > maxY)
                        continue;
                    //wall or self
                    if (shelfs.containsKey(seek) || (x1 == x && y1 == y))
                        continue;
                    entry.getValue().neighbours.add(paths.get(seek));
                }
            }
        }
        
    }

    /**
     * find path form trolley(start) to location next to shelf(end) using A* algorithm
     * @param start starting coordinates (trolley)
     * @param end ending coordinates (shelf)
     * @return Node next to ending location (if path exist)
     */
    public PathNode aStar(Coordinates start, Coordinates end) {
        Queue<PathNode> open = new PriorityQueue<>();
        Queue<PathNode> closed = new PriorityQueue<>();
        if(!paths.containsKey(start))
            return null;
        PathNode startN = paths.get(start);
        open.add(startN);
        startN.update(null,.0);


        while (!open.isEmpty()) {
            PathNode next = open.peek();
            if (next == paths.get(end) || next.getSelf().getDistance(end) == 1) {
                return next;
            }

            for(PathNode node : next.neighbours){
                node.setH(end.getDistance(node.getSelf()));

                if(!open.contains(node) && !closed.contains(node)){
                    node.update(next, next.getG() + next.getSelf().getDistance(node.getSelf()));
                    open.add(node);
                } else if(next.getG() + next.getSelf().getDistance(node.getSelf()) < node.getG()) {
                    node.update(next, next.getG() + next.getSelf().getDistance(node.getSelf()));
                    if(!closed.contains(node)){
                        closed.remove(node);
                        open.add(node);
                    }
                }
            }
            open.remove(next);
            closed.add(next);
        }
        return null;
    }
}
