from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "rajat123"
driver = GraphDatabase.driver(uri, auth=(user, password))
session = driver.session(database="neo4j")

def handle(query):
    result = session.run(query)
    return result.data()


# #Will delete all nodes that have relationship
# query = "match (a) -[r] -> () delete a, r"
# handle(query)


# #Will delete those nodes that dont have relationship
# query = "match (a) delete a"
# handle(query)

#Will create graph-table for us
def create_graph_wannacry():
    query = "match (a) -[r] -> () delete a, r"
    handle(query)

    query = "match (a) delete a"
    handle(query)


    query = """
    call apoc.load.json('12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw_txs_outs.json') yield value
    UNWIND value.ins as ins
    UNWIND value.out as outs
    WITH value, ins, outs
    MERGE (tx:tx {index:value.txid, depth:value.depth_, time_stamp: apoc.date.format(value.time, 's', 'dd/MM/yyyy HH:mm:ss zzz')})
    MERGE (in :output {index: ins.address, label: coalesce(ins.label, "NA")}) 
    MERGE (in)-[p:PAYS {time_stamp: apoc.date.format(value.time, 's', 'dd/MM/yyyy HH:mm:ss zzz'), amount: ins.amount, next_tx: ins.next_tx}]->(tx)
    MERGE (out :output {index: outs.address, label: coalesce(outs.label, "NA")})
    MERGE (tx)-[q:PAYS {time_stamp: apoc.date.format(value.time, 's', 'dd/MM/yyyy HH:mm:ss zzz'), amount: outs.amount, next_tx: coalesce(outs.next_tx, "UNSPENT")}]->(out)
    """
    data = handle(query)
    print("Graph created")
    


#To count the number of nodes
def count():
    query = "MATCH (n) RETURN COUNT(n)"
    return handle(query)

#POST PROCESS FOR UPDATING DEPTH ON ADDRESS NODES
def update_depth():
    query = """MERGE (n:output)-[r:PAYS]-(p:tx)
    WITH n, COALESCE(n.depth, []) + p.depth AS depth
    UNWIND depth as d
    WITH n, collect(distinct d) AS unique
    set n.depth = unique"""
    handle(query)

# casting the 'depth' property into a Long Array
def cast_depth():
    query = """MATCH (n)
    SET n.depth = toIntegerorNull(n.depth)"""
    handle(query)

#.Need to update the transaction nodes (tx) and the payment relationships [:PAYS]
def parse_timestamp():
    query = """MATCH ()-[r:PAYS]->()
    SET r.time_stamp = apoc.date.parse(r.time_stamp,'ms', 'dd/MM/yyyy HH:mm:ss zzz')"""
    handle(query)

def parse_tx():
    query = """MATCH (tx:tx)
    SET tx.time_stamp = apoc.date.parse(tx.time_stamp,'ms', 'dd/MM/yyyy HH:mm:ss zzz')"""
    handle(query)

def format_timestamp():
    query = """MATCH ()-[r:PAYS]->()
    SET r.time_stamp = apoc.date.format(r.time_stamp,'ms', 'dd/MM/yyyy HH:mm:ss zzz')"""
    handle(query)

def format_tx():
    query = """MATCH (tx:tx)
    SET tx.time_stamp = apoc.date.format(tx.time_stamp,'ms', 'dd/MM/yyyy HH:mm:ss zzz')"""
    handle(query)

#Removing a graph if it exists 
def refresh_graph():
    query = """CALL gds.graph.drop('myGraph') YIELD graphName;"""
    handle(query)

# Create the Graph Catalogue - Has to run just once
def create_graph_catalogue():
    query = """CALL gds.graph.project('myGraph', ['output', 'tx'], '*') YIELD graphName, nodeCount, relationshipCount;"""
    return handle(query)


# query = "MATCH (n) RETURN COUNT(n)"
# handle(query)


def pageRank():

    query = """CALL gds.pageRank.write('myGraph', {
    maxIterations: 20,
    dampingFactor: 0.85,
    writeProperty: 'pageRank'
    })"""
    return handle(query)
# pageRank()


#  SET PROPERTIES FOR DEGREE CENTRALITY (IN / OUT DEGREE)
def set_properties_for_degree_centrality():
        query = """
            MATCH (n)
            SET n.out_degree = size([(n)-[:PAYS]->() | n])
            SET n.in_degree = size([(n)<-[:PAYS]-() | n])
            RETURN n.index,n.out_degree, n.in_degree, n.pageRank as pagerank, n.label, n.depth, n.time_stamp
            ORDER by pagerank asc"""
        return handle(query)
# set_properties_for_degree_centrality()


# TOTAL AMOUNT PASSING THROUGH THE TX NODE (IN + OUT)
def total_amount_passing_tx_node():
     
        query = """MATCH (n:output)-[r:PAYS]-(q:tx)
        WITH q, sum(r.amount) as total_btc
        SET q.total_amount = total_btc
        RETURN q.index as txid, total_btc"""
        return handle(query)


# total_amount_passing_tx_node()



# TOTAL AMOUNT PASSING THROUGH THE ADDRESS NODE (IN + OUT)
def total_amount_passing_address_node():
        query = """MATCH (n:output)-[r:PAYS]-(q:tx)
        WITH n, sum(r.amount) as total_btc
        SET n.total_amount = total_btc
        RETURN n.index as btc_addr, total_btc"""
        return handle(query)


# total_amount_passing_address_node()


#Calculating risk rating tx-node 
def risk_rating_txt_node():
      query = """
            MATCH (n)
            SET n.out_degree = size([(n)-[:PAYS]->() | n])
            SET n.in_degree = size([(n)<-[:PAYS]-() | n])
            RETURN n.index,n.out_degree, n.in_degree, n.pageRank as pagerank, n.label, n.depth, n.time_stamp
            ORDER by pagerank asc"""
      session.run(query)
      
      query = """
            MATCH (n)
            WITH sum(n.in_degree+n.out_degree) as total_degrees
            MATCH (q:tx)
            WITH q,(q.in_degree+q.out_degree) as a, total_degrees as td1, q.total_amount as x
            SET q.risk_rating = (toFloat(a) / toFloat(td1)) * (x)
            RETURN q.index, q.risk_rating as risk_rating"""
      return handle(query)

# risk_rating_txt_node()


#Calculating risk rating address-node

def risk_rating_address_node():
        query = """
            MATCH (n)
            SET n.out_degree = size([(n)-[:PAYS]->() | n])
            SET n.in_degree = size([(n)<-[:PAYS]-() | n])
            RETURN n.index,n.out_degree, n.in_degree, n.pageRank as pagerank, n.label, n.depth, n.time_stamp
            ORDER by pagerank asc"""
        session.run(query)

        query = """ MATCH (n)
            WITH sum(n.in_degree+n.out_degree) as total_degrees
            MATCH (q:output)
            WITH q,(q.in_degree+q.out_degree) as a, total_degrees as td1, q.total_amount as x
            SET q.risk_rating = (toFloat(a)/toFloat(td1))*(x)
            RETURN q.index, q.risk_rating as risk_rating"""
        return  handle(query)

# risk_rating_address_node()

# Delete graph
def delete_graph(graph):
      query = f"""CALL gds.graph.drop(\'{graph}\') YIELD graphName;"""
      handle(query)

# delete_graph('addresses_with_transactions_1')
#CREATE ANOTHER GRAPH CATALOG - TO TRAIN THE GRAPH SAGE MODEL
def create_graph_catalog_for_graph_sage_model():
      
    query = """CALL gds.graph.project(
        'addresses_with_transactions_1', 
        {
            output: {
                label: 'output',
                properties: {
                    risk_rating: {
                        property: 'risk_rating',
                        defaultValue: 0
                    },
                    pageRank: {
                        property: 'pageRank',
                        defaultValue: 0
                    },
                    in_degree: {
                        property: 'in_degree',
                        defaultValue: 0
                    },
                    out_degree: {
                        property: 'out_degree',
                        defaultValue: 0
                    },
                    total_amount: {
                        property: 'total_amount',
                        defaultValue: 0
                    }
                }
            },
            tx: {
                label: 'tx',
                properties: {
                    risk_rating: {
                        property: 'risk_rating',
                        defaultValue: 0
                    },
                    pageRank: {
                        property: 'pageRank',
                        defaultValue: 0
                    },
                    in_degree: {
                        property: 'in_degree',
                        defaultValue: 0
                    },
                    out_degree: {
                        property: 'out_degree',
                        defaultValue: 0
                    },
                    total_amount: {
                        property: 'total_amount',
                        defaultValue: 0
                    }
                }
            }
        },
        {
            PAYS: {
                type: 'PAYS',
                orientation: 'NATURAL',
                properties: {
                    amount: {
                        property: 'amount',
                        defaultValue: 0
                    }
                }
            }
        }
    )
    YIELD graphName, nodeCount, relationshipCount;"""
    return handle(query)

#Delete model 
def delete_model(model):
    query = f"""CALL gds.beta.model.drop(\'{model}\')"""
    handle(query)

# delete_model('weightedTrainedModel')


def train_graph_sage_model ():

    query = """CALL gds.beta.graphSage.train(
    'addresses_with_transactions_1',
    {
        modelName: 'weightedTrainedModel',
        featureProperties: ['pageRank', 'risk_rating', 'in_degree', 'out_degree', 'total_amount'],
        aggregator: 'mean',
        activationFunction: 'sigmoid',
        sampleSizes: [25, 10],
        relationshipWeightProperty: 'amount',
        relationshipTypes: ['PAYS']
    }
    )"""

    handle(query)

# train_graph_sage_model()


#Testing different hyperparameters on graph sage model 
def test_different_hp_graph_sage():
      query = """
                CALL gds.beta.graphSage.train('addresses_with_transactions_1',{
                modelName:'testModel',
                aggregator:'pool',
                batchSize:512,
                activationFunction:'relu',
                epochs:10,
                sampleSizes:[25,10],
                learningRate:0.0000001,
                embeddingDimension:256,
                featureProperties:['pageRank', 'risk_rating', 'in_degree', 'out_degree', 'total_amount']})
                YIELD modelInfo
                RETURN modelInfo
"""
      handle(query)

#Delete exisiting model if any 
# delete_model('testModel')

# test_different_hp_graph_sage()



#-Trying the FastRP embedding algorithm
def FastRP():
      query = """
        CALL gds.fastRP.stream('addresses_with_transactions_1',{
            relationshipTypes:['PAYS'],
            featureProperties: ['pageRank', 'risk_rating', 'in_degree', 'out_degree', 'total_amount'], //5 node features
            relationshipWeightProperty: 'amount',
            embeddingDimension: 250,
            iterationWeights: [0, 0, 1.0, 1.0],
            normalizationStrength:0.05
            //writeProperty: 'fastRP_Extended_Embedding'
        })
        YIELD nodeId, embedding
        RETURN gds.util.asNode(nodeId).index as name, gds.util.asNode(nodeId).risk_rating as exp, gds.util.asNode(nodeId).pageRank as pr, gds.util.asNode(nodeId).out_degree as outdeg, gds.util.asNode(nodeId).in_degree as indeg, gds.util.asNode(nodeId).total_amount as ta, gds.util.asNode(nodeId).time_stamp as ts, embedding as features"""

      return handle(query)

# FastRP()

#Stream embeddings
def stream_embeddings():
      query = """CALL gds.beta.graphSage.stream(
                    'addresses_with_transactions_1',
                    {
                        modelName: 'weightedTrainedModel'
                    }
                    )"""
      handle(query)
# stream_embeddings()



# STREAM embeddings with respective properties
# output to the file 20210311_GraphSAGE_embeddings.csv
def stream_embeddings_with_properties():
    query = """CALL gds.beta.graphSage.stream(
    'addresses_with_transactions_1',
    {
        modelName: 'testModel'
    }
    )
    YIELD nodeId, embedding
    RETURN gds.util.asNode(nodeId).index as name, gds.util.asNode(nodeId).risk_rating as exp, gds.util.asNode(nodeId).pageRank as pr, gds.util.asNode(nodeId).out_degree as outdeg, gds.util.asNode(nodeId).in_degree as indeg, gds.util.asNode(nodeId).total_amount as ta, gds.util.asNode(nodeId).time_stamp as ts, embedding as features"""
    handle(query)

stream_embeddings_with_properties()
