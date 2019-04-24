
import React, { Component } from 'react'
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import { withStyles } from '@material-ui/core';
import { getTerms } from '../services/TermService'
import { getJobs } from '../services/JobService'
const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing.unit * 2,
  },
});


class MainPage extends Component {
  constructor() {
    super()
    this.state = {
      terms: [],
      term: '',
      jobs: [],
      selectedTerm: null
    }
    this.getTerms = this.getTerms.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  async getTerms() {
    try {
      const res = await getTerms()
      let terms = []
      if (res.status == 200) {
        terms = res.data  
      }
      
      console.log(terms)
      this.setState({
        terms
      })
    } catch (e) {
      console.error(e)
      throw e
    }
  }

  async getJobs(termId) {
    try {
      const res = await getJobs(termId)
      let jobs = null
      if(res.status == 200){
        jobs = res.data
      }
      console.log(jobs)
      this.setState([
        jobs
      ])
      
    } catch (e) {
      console.error(e)
      throw e
    }
  }

  handleChange(event) {
    console.log(event.target)
    this.setState({ [event.target.name]: event.target.value });
    this.getJobs(event.target.value)
  }

  componentDidMount() {
    this.getTerms()
  }
  render() {
    const {
      classes
    } = this.props

    const {
      terms
    } = this.state
    return (
      <FormControl className={classes.formControl}>
        <InputLabel htmlFor="age-simple">Term</InputLabel>
        <Select
          value={this.state.term}
          onChange={this.handleChange}
          inputProps={{
            name: 'term',
            id: 'term',
          }}
        >
          <MenuItem value="">
            <em>Select a term</em>
          </MenuItem>
          {terms.map(term => (
            <MenuItem value={term.id} key={term.id}>{term.term}</MenuItem>
          ))}
        </Select>
      </FormControl>
    )

  }
}

export default withStyles(styles)(MainPage)