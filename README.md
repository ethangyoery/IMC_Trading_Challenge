# IMC_Trading_Challenge
Making Easy Shells

Trading Method

Talked to Keegan (my brother), his suggestions:

- reverse weighted spot for inital valuation
- use successful trades from previous rounds to slightly influence valuation (older the trade less influence)
- don't trade on the base book (base product i.e. one of the items), use the relationship between the books
  to trade on the related book and use the base book to position manage (see example:)
  - base book (shells) intially valued at 10
  - related book (bananas) valued at 2 * shells (initally 20)
  - say bananas are being sold at 19, our valuation tells us to buy at 19 because we think they're worth 20, so we buy lets say 1
  - to manage our position and 'lock in' our money, we do the oppsoite in the base book (shells) and sell the same amount ($20 worth) i.e. sell 2 shells
  - the overall earnings is $1 because sold $20 and spent $19
  - the oppsoite cause can also happen where if we sell in the related book (bananas), then we buy the same amount in the base book (shells)
               
- Theres a lot more other stuff Keegan told me about but he said this was a good starting point and to try it out
