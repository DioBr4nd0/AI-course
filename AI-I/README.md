# MMR Results

## 1st Walkthrough

Results Comparison (100,000 dataset) (MMR Wins):

```bash
$ python parser.py

Loading 1 Lakh (100,000) news articles...

Initializing embeddings on Nvidia GPU (CUDA)...

Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.

Loading weights: 100%|██████████████████████████████████████████████████████| 103/103 [00:00<00:00, 1561.29it/s, Materializing param=pooler.dense.weight]

BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2

Key                     | Status     |  |
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  |

Notes:
- UNEXPECTED    :can be ignored when loading from different task/architecture; not ok if you expect identical arch.

Building FAISS index (This will take a moment for 100k items)...

============================================================
🔍 STANDARD RAG (Sending 10 chunks to the LLM = HIGH COST)
============================================================

--- Result 1 ---
PeopleSoft Says Its Board May Consider an Oracle Takeover Offer PeopleSoft Inc. said it's willing to discuss a bid by Oracle Corp. at the right 'price, the first time officials have raised the possibility of ending the companies 16-month takeover fight.

--- Result 2 ---
Update: Oracle makes 'final' PeopleSoft offer, raises bid NOVEMBER 01, 2004 (COMPUTERWORLD) - The end may be in sight in the ongoing saga of Oracle Corp.'s hostile takeover bid for embattled competitor PeopleSoft Inc.

--- Result 3 ---
Majority of PeopleSoft shareholders accept Oracle bid The tender result is a blow to PeopleSoft, which hoped to see Oracle's 17-month takeover campaign end at midnight last night. Oracle had pledged to withdraw its offer if it did not receive backing from a majority of PeopleSoft's shareholders.

--- Result 4 ---
PeopleSoft nearly positive towards Oracle bid PeopleSoft said it could accept a takeover bid from Oracle and now needs time to weigh on it. Oracle has been haunting PeopleSoft for 15 months with the possible bid of $7.

--- Result 5 ---
Oracle Raises PeopleSoft Bid by 14 to $8.8 Billion (Update5) Oracle Corp. raised its takeover offer for PeopleSoft Inc. by 14 percent to $8.8 billion, increasing the pressure on the smaller software company to give up its 17-month fight against the bid.

--- Result 6 ---
Oracle extends PeopleSoft takeover bid Oracle Corp. has extended its $7.7 billion hostile takeover bid for Pleasanton's PeopleSoft Inc. until Sept. 10. Redwood City-based Oracle's previous offer would have expired at 9 pm Friday.

--- Result 7 ---
PeopleSoft Says Again Oracle Bid Inadequate, It Won't Sell PeopleSoft Inc. said its board remains convinced Oracle Inc.'s $24-a-share takeover bid is inadequate and said it will not sell the company for less than it's worth.

--- Result 8 ---
Oracle poised to pounce on PeopleSoft BOLSTERED by investors, Oracle appears set to complete its long-sought takeover of PeopleSoft, unless its rival proves it is worth more than the $US9.2 billion ($11.7 billion) bid currently on the table.

--- Result 9 ---
PeopleSoft Ousts CEO Who Battled Oracle In NEW YORK story headlined "PeopleSoft ousts CEO amid battle with Oracle," please read in paragraph 5, "Oracle launched its surprise takeover bid in June 2003" ... instead of "PeopleSoft launched .. )

--- Result 10 ---
As software world awaits ruling, Oracle extends offer With the future of its $7.7 billion takeover attempt of PeopleSoft Inc. resting in the hands of a federal judge, Oracle Corp. is once again extending its tender offer for investors to tender their shares.

... plus 7 more highly similar chunks sent to the LLM.

============================================================
🔀 MMR RAG (Sending 3 diverse chunks to the LLM = LOW COST)
============================================================

--- Result 1 ---
PeopleSoft Says Its Board May Consider an Oracle Takeover Offer PeopleSoft Inc. said it's willing to discuss a bid by Oracle Corp. at the right 'price, the first time officials have raised the possibility of ending the companies 16-month takeover fight.

--- Result 2 ---
PeopleSoft Ousts CEO Who Battled Oracle In NEW YORK story headlined "PeopleSoft ousts CEO amid battle with Oracle," please read in paragraph 5, "Oracle launched its surprise takeover bid in June 2003" ... instead of "PeopleSoft launched .. )

--- Result 3 ---
Majority of PeopleSoft shareholders accept Oracle bid The tender result is a blow to PeopleSoft, which hoped to see Oracle's 17-month takeover campaign end at midnight last night. Oracle had pledged to withdraw its offer if it did not receive backing from a majority of PeopleSoft's shareholders.
```

## 2nd Walkthrough

Results Comparison (15,000 dataset) (Standard RAG wins):

```bash
============================================================
🔍 STANDARD RAG RESULTS (Similarity Only)
============================================================

--- Result 1 ---
Apache Spark is an open-source unified analytics engine for large-scale data processing. Spark provides an interface for programming clusters with implicit data parallelism and fault tolerance. Originally developed at the University of California, Be...

--- Result 2 ---
Apache Spark requires a cluster manager and a distributed storage system. For cluster management, Spark supports standalone (native Spark cluster, where you can launch a cluster either manually or use the launch scripts provided by the install packag...

--- Result 3 ---
Apache Spark has its architectural foundation in the resilient distributed dataset (RDD), a read-only multiset of data items distributed over a cluster of machines, that is maintained in a fault-tolerant way. The Dataframe API was released as an abst...

============================================================
🔀 MMR RAG RESULTS (Similarity + Diversity)
============================================================

--- Result 1 ---
Apache Spark is an open-source unified analytics engine for large-scale data processing. Spark provides an interface for programming clusters with implicit data parallelism and fault tolerance. Originally developed at the University of California, Be...

--- Result 2 ---
A computer worm is a standalone malware computer program that replicates itself in order to spread to other computers. It often uses a computer network to spread itself, relying on security failures on the target computer to access it. It will use th...

--- Result 3 ---
Kafka stores key-value messages that come from arbitrarily many processes called producers. The data can be partitioned into different "partitions" within different "topics". Within a partition, messages are strictly ordered by their offsets (the pos...
```
