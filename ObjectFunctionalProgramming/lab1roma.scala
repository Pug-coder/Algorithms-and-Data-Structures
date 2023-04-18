object Main {
	def sorted(compare: (Int, Int) => Boolean): List[Int] => Boolean = {
		def isSorted(xs: List[Int]): Boolean = xs match {
			case Nil => true
			case x :: Nil => true
			case x :: y :: ys => 
				if (!compare(x, y)) false
				else isSorted(y :: ys) 
		}
		isSorted
	}


	def main(args: Array[String]): Unit = {
		val ascSort = sorted((x, y) => x <= y)
		val descSort = sorted((x, y) => x >= y)
		val list1 = List(1, 2, 3, 4, 5)
		val list2 = List(5, 4, 3, 2, 1)
		println(ascSort(list1)) // true
		println(descSort(list1)) // false
		println(ascSort(list2)) // false
		println(descSort(list2)) // true
	}
}