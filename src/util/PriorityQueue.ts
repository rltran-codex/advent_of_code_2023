interface IPriorityQueue<T> {
  push(node: T): void;
  pop(): T;
  size(): number;
  isEmpty(): boolean;
}

/*
 * to use priority queue for this problem,
 * create a priority queue like so:
 *
 * const pq = new MinHeap(function(a, b) { return a.heatValue > b.heatValue });
 */
export class PriorityQueue<T> implements IPriorityQueue<T> {
  private _minHeap: T[];
  private _comparator?: (a: T, b: T) => boolean;

  /*
   * Used to grab the indexes of a node in the priority queue 
   */
  left     = (idx: number) => 2 * idx + 1;
  right    = (idx: number) => 2 * idx + 1;
  parent   = (idx: number) => Math.floor((idx - 1) / 2);
  hasLeft  = (idx: number) => this.left(idx) < this._minHeap.length;
  hasRight = (idx: number) => this.right(idx) < this._minHeap.length;

  constructor(comparator?: (a: T, b: T) => boolean) {
    this._minHeap = [];
    this._comparator = comparator;
  }

  push(node: T) {
    this._minHeap.push(node); // insert new child at the end of the heap
    // move the child up until you reach the root node and the heap property is satisfied
    let cIdx = this.size() - 1;
    let pIdx = this.parent(cIdx);
    while (cIdx > 0 && this._compare(this._minHeap[pIdx], this._minHeap[cIdx])) {
      this._swap(cIdx, pIdx);
      cIdx = pIdx;
    }
  }

  pop(): T {
    if (this.isEmpty()) {
      return null;
    }

    // swap first and last element first
    this._swap(0, this.size() - 1);
    const n = this._minHeap[this.size() - 1];
    this._minHeap.pop();
    this.heapify(0);
    return n;
  }

  private heapify(idx: number) {
    const mid = Math.floor(this.size() / 2);
    
    while (idx <= mid - 1) {
      let left = this.left(idx);
      let right = this.right(idx);
      let min = left;

      if (this.hasRight(idx) && this._compare(this._minHeap[left], this._minHeap[right])) {
        min = right;
      }

      if (this._compare(this._minHeap[idx], this._minHeap[min])) {
        this._swap(idx, min);
      }

      idx = min;
    }
  }

  private _swap(idx1: number, idx2: number) {
    const temp = this._minHeap[idx1];
    this._minHeap[idx1] = this._minHeap[idx2];
    this._minHeap[idx2] = temp;
  }


  size(): number {
    return this._minHeap.length;
  }

  isEmpty(): boolean {
    return this._minHeap.length === 0;
  }

  private _compare(a: T, b: T) {
    if (this._comparator) {
      return this._comparator(a, b);
    }

    return a > b;
  }
}