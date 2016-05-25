# Delver
### Yet Another Magic Card Search Engine

The initial impetus for this was a flurry of requests from users at the Magic-centric web forum [No Goblins Allowed](http://forum.nogoblinsallowed.com).  They had created a wide variety of custom card sets and were interested in playing tournaments using those cards, but deck construction is extremely difficult if the only way you have to find a card that fills a particular role is to look over the entire list, every time.

So, I very quickly threw together [an implementation](http://forum.nogoblinsallowed.com/card_search.php) built into the forum software. This was nice and easy to do, but has the obvious and major problems associated with being built into PhpBB.

This project is my attempt to fix those issues by rebuilding the tool in with a modern interface, non-PHP backend, and other features I've wished for a few times:
 - shorthand syntax for quicker searching, a la [magiccards.info](http://magiccards.info)
 - live feedback for faster exploration, as with [Hunter](http://mtg-hunter.com/)

And, as long as we have that, might as well allow searching over real cards, too!
