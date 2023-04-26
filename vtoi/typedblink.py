from typedb.client import *

with TypeDB.core_client("localhost:1729") as client:
    with client.session("latest_imia", SessionType.DATA) as session:


        ### Read the person using a READ only transaction
        #with session.transaction(TransactionType.READ) as read_transaction:
        #    read_transaction.query().match('match $concept isa Performer, has UID "1234";')
        #with session.transaction(TransactionType.READ) as read_transaction:
        #    read_transaction.query().delete('delete $concept has "1234";')

        #with session.transaction(TransactionType.WRITE) as write_transaction:

        session.transaction(TransactionType.WRITE).query().update('match $concept isa Performer, has UID "1234"; delete $concept isa Performer, has UID "1234";insert $concept isa Performer, has UID "1111";')

        session.transaction(TransactionType.WRITE).commit()

        ## if not using a `with` statement, then we must always close the session and the read transaction
        # read_transaction.close()
        # session.close()
        # client.close()




