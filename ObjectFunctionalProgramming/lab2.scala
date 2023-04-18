class MultSet (ar: Set[Int], kr: Int){
	var sett = ar.map(_ * kr)
	var k = kr

	def + (s: MultSet) = new MultSet(sett union s.sett, 1)

	def * (s: MultSet) = new MultSet(sett intersect s.sett, 1)

	def in (c: Int) = sett contains c 
}

object Lab2 {
	def main(args: Array[String]) = {
		
		val s = new MultSet(Set(1,2,3,4,5), 2)
		println(s.sett)
		val new_set = new MultSet(Set(6,5,7,8,9), 2)
		println(new_set.sett)

		println("___________Union___________")
		println((s + new_set).sett)

		println("_______Intersection________")
		println((s * new_set).sett)
		
		println("_________contains__________")
		val c = 2
		println(s in c)
	}
}
