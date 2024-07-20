# Beanie ORM

from beanie import Document, Optional, init_beanie

class User(Document):
    name: str
    region: str
    income: list #because there are multiple income sources so they must be labeled too example: [[job, ammount]] 
    debt: list #because there are multiple debts so they must be labeled too example: [[credit card, ammount]]
    expenses: list #because there are multiple expenses so they must be labeled too example: [[rent, ammount]]
    #now I need an investments field that is optional
    investments: Optional[list] #because there are multiple investments so they must be labeled too example: [[stock, ammount]]   
    goals: Optional[list] #because there are multiple goals so they must be labeled too example: [[buy a house, ammount]]
    milestones: Optional[list] #because there are multiple milestones so they must be labeled too example: [[buy a house, ammount]]
    