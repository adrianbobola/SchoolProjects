/*
  Class PathNode
  @author Ladislav Dokoupil (xdokou14)
  @author Adrián Bobola (xbobol00)
 */
package ija21;

import java.util.*;

class PathNode implements Comparable<PathNode> {
    private Coordinates self;
    private PathNode parent;
    //distance from finish
    private Double h = Double.MAX_VALUE;
    //distance from start
    private Double g = Double.MAX_VALUE;

    List<PathNode> neighbours = new ArrayList<>();

    /**
     * Initalize Node with given cordinates for path finding
     * @param self Node cordinates
     */
    public PathNode(Coordinates self){
        this.self = self;
    }

    /**
     * Update Nodes parent and g cost
     * @param parent Node of new parent of node
     * @param g new Node g cost (shortest found distance from start)
     */
    public void update(PathNode parent, double g){
        this.g = g;
        this.parent = parent;
    }

    /**
     * Calculate Node heuristic used by pathfinding algorithm
     * @return Node path cost
     */
    public Double heuristic(){
        return g+h;
    }

    /**
     * Used to compare Nodes by path cost
     * @param node node to compare to
     * @return diference in node costs
     */
    @Override
    public int compareTo(PathNode node) {
        return (int) (this.heuristic() - node.heuristic());
    }

    public Coordinates getSelf() {
        return self;
    }

    public PathNode getParent() {
        return parent;
    }

    public Double getH() {
        return h;
    }
    public void setH(Double h) {
        this.h = h;
    }

    public Double getG() {
        return g;
    }

}