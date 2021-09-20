--
-- PostgreSQL database dump
--

-- Dumped from database version 10.16
-- Dumped by pg_dump version 10.16

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE findmyvmdb; Type: COMMENT; Schema: -; Owner: findmyvmuser
--

COMMENT ON DATABASE findmyvmdb IS 'https://roweb.cec.lab.emc.com/findmyvm';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: f_cecavc(); Type: FUNCTION; Schema: public; Owner: findmyvmuser
--

CREATE FUNCTION public.f_cecavc() RETURNS bigint
    LANGUAGE sql
    AS $$select count(*) from vc where type = 'cec-a'$$;


ALTER FUNCTION public.f_cecavc() OWNER TO findmyvmuser;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: bk_2018; Type: TABLE; Schema: public; Owner: findmyvmuser
--

CREATE TABLE public.bk_2018 (
    scandate timestamp without time zone,
    vm character varying(64),
    config_name character varying(128),
    config_vmpathname character varying(256),
    config_guestfullname character varying(128),
    runtime_powerstate character varying(64),
    guest_ipaddress character varying(64),
    guest_toolsstatus character varying(64),
    runtime_host_name character varying(64),
    config_memorysizemb integer,
    config_numcpu integer,
    vc character varying(128),
    parent_name character varying(128),
    nic_macaddress character varying(2048),
    nic_ipaddress character varying(2048)
);


ALTER TABLE public.bk_2018 OWNER TO findmyvmuser;

--
-- Name: bk_2019; Type: TABLE; Schema: public; Owner: findmyvmuser
--

CREATE TABLE public.bk_2019 (
    scandate timestamp without time zone,
    vm character varying(64),
    config_name character varying(128),
    config_vmpathname character varying(256),
    config_guestfullname character varying(128),
    runtime_powerstate character varying(64),
    guest_ipaddress character varying(64),
    guest_toolsstatus character varying(64),
    runtime_host_name character varying(64),
    config_memorysizemb integer,
    config_numcpu integer,
    vc character varying(128),
    parent_name character varying(128),
    nic_macaddress character varying(2048),
    nic_ipaddress character varying(2048)
);


ALTER TABLE public.bk_2019 OWNER TO findmyvmuser;

--
-- Name: bk_2020; Type: TABLE; Schema: public; Owner: findmyvmuser
--

CREATE TABLE public.bk_2020 (
    scandate timestamp without time zone,
    vm character varying(64),
    config_name character varying(128),
    config_vmpathname character varying(256),
    config_guestfullname character varying(128),
    runtime_powerstate character varying(64),
    guest_ipaddress character varying(64),
    guest_toolsstatus character varying(64),
    runtime_host_name character varying(64),
    config_memorysizemb integer,
    config_numcpu integer,
    vc character varying(128),
    parent_name character varying(128),
    nic_macaddress character varying(2048),
    nic_ipaddress character varying(2048),
    uuid character varying(40),
    instanceuuid character varying(40)
);


ALTER TABLE public.bk_2020 OWNER TO findmyvmuser;

--
-- Name: esxi; Type: TABLE; Schema: public; Owner: findmyvmuser
--

CREATE TABLE public.esxi (
    scandate timestamp without time zone,
    vc character varying(128),
    host character varying(128),
    hardware_model character varying(128),
    hardware_vendor character varying(128),
    config_name character varying(128),
    config_product_full_name character varying(128),
    overall_status character varying(128),
    uuid character varying(128),
    assettag character varying(128),
    memorysize character varying(128),
    biosversion character varying(128),
    bios_releasedate character varying(128),
    ipaddress character varying(128)
);


ALTER TABLE public.esxi OWNER TO findmyvmuser;

--
-- Name: v_cec_hosts; Type: VIEW; Schema: public; Owner: findmyvmuser
--

CREATE VIEW public.v_cec_hosts AS
 SELECT esxi.vc,
    esxi.uuid,
    esxi.assettag,
    esxi.ipaddress,
    esxi.hardware_model AS hw,
    esxi.hardware_vendor AS vendor,
    esxi.config_name AS hostname,
    esxi.config_product_full_name AS version
   FROM public.esxi
  WHERE ((esxi.scandate > ( SELECT to_date(to_char(esxi_1.scandate, 'YYYY-MM-DD'::text), 'YYYY-MM-DD'::text) AS latest_scandate
           FROM public.esxi esxi_1
          ORDER BY esxi_1.scandate DESC
         LIMIT 1)) AND ((esxi.vc)::text ~~* '%cec%'::text));


ALTER TABLE public.v_cec_hosts OWNER TO findmyvmuser;

--
-- Name: vc; Type: TABLE; Schema: public; Owner: findmyvmuser
--

CREATE TABLE public.vc (
    vc_host character varying(128) NOT NULL,
    vc_user character varying(64) NOT NULL,
    vc_pwd character varying(64) NOT NULL,
    ignore boolean,
    scandate timestamp without time zone,
    type character varying(8),
    failcount integer DEFAULT 0
);


ALTER TABLE public.vc OWNER TO findmyvmuser;

--
-- Name: v_problem_vcs; Type: VIEW; Schema: public; Owner: findmyvmuser
--

CREATE VIEW public.v_problem_vcs AS
 SELECT vc.vc_host,
    vc.vc_user,
    vc.vc_pwd,
    vc.ignore,
    vc.scandate,
    vc.type,
    vc.failcount
   FROM public.vc
  WHERE (vc.failcount > 3);


ALTER TABLE public.v_problem_vcs OWNER TO findmyvmuser;

--
-- Name: vclog; Type: TABLE; Schema: public; Owner: findmyvmuser
--

CREATE TABLE public.vclog (
    vc_host character varying(128),
    scandate timestamp without time zone,
    good boolean,
    reason character varying(128)
);


ALTER TABLE public.vclog OWNER TO findmyvmuser;

--
-- Name: vms; Type: TABLE; Schema: public; Owner: findmyvmuser
--

CREATE TABLE public.vms (
    scandate timestamp without time zone,
    vm character varying(64),
    config_name character varying(128),
    config_vmpathname character varying(256),
    config_guestfullname character varying(128),
    runtime_powerstate character varying(64),
    guest_ipaddress character varying(64),
    guest_toolsstatus character varying(64),
    runtime_host_name character varying(64),
    config_memorysizemb integer,
    config_numcpu integer,
    vc character varying(128),
    parent_name character varying(128),
    nic_macaddress character varying(2048),
    nic_ipaddress character varying(2048),
    uuid character varying(40),
    instanceuuid character varying(40)
);


ALTER TABLE public.vms OWNER TO findmyvmuser;

--
-- Name: vms_test; Type: TABLE; Schema: public; Owner: findmyvmuser
--

CREATE TABLE public.vms_test (
    scandate timestamp without time zone,
    vm character varying(64),
    config_name character varying(128),
    config_vmpathname character varying(256),
    config_guestfullname character varying(128),
    runtime_powerstate character varying(64),
    guest_ipaddress character varying(64),
    guest_toolsstatus character varying(64),
    runtime_host_name character varying(64),
    config_memorysizemb integer,
    config_numcpu integer,
    vc character varying(128),
    parent_name character varying(128),
    nic_macaddress character varying(2048),
    nic_ipaddress character varying(2048),
    instanceuuid character(40),
    uuid character(40)
);


ALTER TABLE public.vms_test OWNER TO findmyvmuser;

--
-- Name: vc vc_pkey; Type: CONSTRAINT; Schema: public; Owner: findmyvmuser
--

ALTER TABLE ONLY public.vc
    ADD CONSTRAINT vc_pkey PRIMARY KEY (vc_host);


--
-- Name: vms_config_name_idx; Type: INDEX; Schema: public; Owner: findmyvmuser
--

CREATE INDEX vms_config_name_idx ON public.vms USING btree (config_name);


--
-- Name: vms_nic_macaddress_idx; Type: INDEX; Schema: public; Owner: findmyvmuser
--

CREATE INDEX vms_nic_macaddress_idx ON public.vms USING btree (nic_macaddress);


--
-- Name: vms_parent_name_idx; Type: INDEX; Schema: public; Owner: findmyvmuser
--

CREATE INDEX vms_parent_name_idx ON public.vms USING btree (parent_name);


--
-- PostgreSQL database dump complete
--

