class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        if(numExchange>numBottles):
            return numBottles
        else:
            add=numBottles
            while(numBottles>=numExchange):
                numBottles-=numExchange
                add+=1
                numBottles+=1
            return add

        